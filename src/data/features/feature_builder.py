import os
import pandas as pd
from sqlalchemy import text
from typing import Dict, Any

class FeatureQueryBuilder:
  """SQL 파일을 자동 탐색하고, 설정 기반으로 동적 JOIN 쿼리를 빌드합니다.

  이 클래스는 'dql' 폴더에 있는 여러 SQL 조각(피처 정의)들을 자동으로
  탐색합니다. 그리고 주어진 설정(join_config)에 따라 CTE(Common Table
  Expression)를 사용하여 단일 SQL 쿼리를 동적으로 생성하고 실행합니다.

  Attributes:
    db_handler (DBHandler): 데이터베이스 연결을 관리하는 DBHandler 인스턴스.
    sql_root_path (str): SQL 파일들이 있는 루트 디렉토리 경로.
    available_features (dict): 탐색된 모든 피처의 이름과 파일 경로 맵.
  """
  def __init__(self, db_handler: Any, sql_root_path: str = 'sql'):
    """FeatureQueryBuilder 인스턴스를 초기화합니다.

    Args:
      db_handler (DBHandler): 데이터베이스 연결 및 실행을 위한 DBHandler 객체.
      sql_root_path (str): SQL 파일들의 최상위 루트 디렉토리. 기본값은 'sql'입니다.
    """
    self.db_handler = db_handler
    # 이 파일의 위치를 기준으로 sql_root_path의 절대 경로를 계산합니다.
    self.sql_root_path = os.path.abspath(os.path.join(
      os.path.dirname(__file__), '..', sql_root_path
    ))
    self.available_features = self._discover_features()
    print(f"✅ 총 {len(self.available_features)}개의 사용 가능한 피처(.sql)를 탐색했습니다.")

  def _discover_features(self) -> Dict[str, str]:
    """sql_root_path 하위의 모든 'dql' 폴더에서 .sql 파일을 탐색합니다.

    Returns:
      Dict[str, str]: {피처 이름: 파일 전체 경로} 형태의 딕셔너리.
          피처 이름은 .sql 확장자를 제외한 파일명입니다.
    """
    features = {}
    for root, _, files in os.walk(self.sql_root_path):
      if os.path.basename(root) == 'dql':
        for file in files:
          if file.endswith('.sql'):
            feature_name = os.path.splitext(file)[0]
            features[feature_name] = os.path.join(root, file)
    return features

  def build(self, join_config: Dict[str, Any], start_date: str, end_date: str) -> pd.DataFrame:
    """설정(join_config)을 기반으로 최종 SQL 쿼리를 빌드하고 실행합니다.

    Args:
      join_config (Dict[str, Any]): 어떤 피처를 어떻게 JOIN할지 정의한
        설정 딕셔너리. 'base_table'과 'join_tables' 키를 포함해야 합니다.
      start_date (str): 조회 시작일 (YYYYMMDD).
      end_date (str): 조회 종료일 (YYYYMMDD).

    Returns:
      pd.DataFrame: 모든 피처가 JOIN된 최종 결과 데이터프레임.

    Raises:
      ValueError: join_config에 명시된 피처를 self.available_features에서
        찾을 수 없는 경우 발생합니다.
    """
    # 1. 설정에 명시된 피처들로 CTE 파트 생성
    cte_parts = []
    base_table_name = join_config['base_table']
    all_feature_names = [base_table_name] + [item['name'] for item in join_config['join_tables']]

    for name in all_feature_names:
      if name not in self.available_features:
        raise ValueError(f"'{name}' 피처를 찾을 수 없습니다. '{name}.sql' 파일이 dql 폴더에 있는지 확인하세요.")
      
      with open(self.available_features[name], 'r', encoding='utf-8') as f:
        sql_snippet = f.read()
      cte_parts.append(f"{name} AS (\n{sql_snippet}\n)")

    # 2. 설정을 기반으로 JOIN 로직 동적 생성
    base_alias = "t_base"
    join_clauses = [f"FROM {base_table_name} AS {base_alias}"]
    select_columns = [f"{base_alias}.*"]

    for i, table_info in enumerate(join_config['join_tables']):
      alias = f"t{i+1}"
      on_conditions = " AND ".join([f"{base_alias}.{key} = {alias}.{key}" for key in table_info['on']])
      join_clauses.append(f"LEFT JOIN {table_info['name']} AS {alias} ON {on_conditions}")
      for col in table_info['columns']:
        select_columns.append(f"{alias}.{col}")
    
    # 3. 최종 쿼리 조립
    final_query = f"""
    WITH {', '.join(cte_parts)}
    SELECT {', '.join(select_columns)}
    {' '.join(join_clauses)}
    ORDER BY {base_alias}.date, {base_alias}.code
    """

    # 4. 쿼리 실행
    params = {"start_date": start_date, "end_date": end_date}
    return pd.read_sql_query(sql=text(final_query), con=self.db_handler.engine, params=params)