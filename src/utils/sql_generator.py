# src/utils/sql_generator.py
import inspect
import re
from dataclasses import fields, is_dataclass
from types import ModuleType
from typing import Type, Any, Dict, List

class SQLGenerator:
  """
  데이터클래스 스키마를 동적으로 분석하여,
  PostgreSQL에 맞는 CREATE 및 UPSERT SQL문을 자동으로 생성하는 클래스.
  """

  def __init__(self, schemas_module: ModuleType):
    """
    스키마 모듈을 입력받아 내부에 정의된 모든 데이터클래스를 로드합니다.
    
    Args:
        schemas_module (ModuleType): @dataclass가 정의된 파이썬 모듈
    """
    self.schemas: Dict[str, Type[Any]] = self._discover_dataclasses(schemas_module)
    print(f"✅ {len(self.schemas)}개의 데이터클래스 스키마를 성공적으로 로드했습니다.")

  def _discover_dataclasses(self, module: ModuleType) -> Dict[str, Type[Any]]:
    """모듈 내에서 모든 데이터클래스를 찾아 딕셔너리로 반환합니다."""
    found_schemas = {}
    for name, obj in inspect.getmembers(module):
      # is_dataclass()는 @dataclass로 정의된 클래스인지 확인합니다.
      if is_dataclass(obj):
        # 동일한 이름의 클래스가 중복 정의된 경우, 파일의 더 마지막에 정의된 것을 사용합니다.
        # 이는 수정된 최종 버전을 채택하기 위함입니다.
        if name not in found_schemas or \
          inspect.getsourcelines(obj)[1] > inspect.getsourcelines(found_schemas[name])[1]:
          found_schemas[name] = obj
    return found_schemas

  def _map_type(self, py_type: Type[Any]) -> str:
    """Python 타입을 PostgreSQL 타입으로 변환합니다."""
    type_mapping = {
      str: "TEXT",
      int: "INTEGER",
      float: "REAL",
    }
    return type_mapping.get(py_type, "TEXT") # 매핑에 없는 타입은 TEXT로 기본 처리

  def _to_snake_case(self, name: str) -> str:
    """CamelCase 클래스 이름을 snake_case 테이블 이름으로 변환합니다."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

  def get_available_schemas(self) -> List[str]:
    """로드된 모든 스키마의 이름을 리스트로 반환합니다."""
    return list(self.schemas.keys())

  def generate_create_sql(self, schema_name: str, primary_key: str = 'ticker') -> str:
    """데이터클래스 이름을 기반으로 CREATE TABLE SQL문을 생성합니다."""
    if schema_name not in self.schemas:
      raise ValueError(f"'{schema_name}' 스키마를 찾을 수 없습니다.")
    
    dataclass = self.schemas[schema_name]
    table_name = self._to_snake_case(schema_name)
    
    columns = ["id SERIAL PRIMARY KEY"]
    for field in fields(dataclass):
      col_name = field.name
      sql_type = self._map_type(field.type)
      constraints = f"UNIQUE NOT NULL" if col_name == primary_key else ""
      columns.append(f"{col_name} {sql_type} {constraints}".strip())
    
    columns.append("updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP")
    
    columns_str = ",\n  ".join(columns)
    return f"CREATE TABLE IF NOT EXISTS {table_name} (\n  {columns_str}\n);"

  def generate_upsert_sql(self, schema_name: str, conflict_key: str = 'ticker') -> str:
    """데이터클래스 이름을 기반으로 UPSERT (INSERT ON CONFLICT) SQL문을 생성합니다."""
    if schema_name not in self.schemas:
      raise ValueError(f"'{schema_name}' 스키마를 찾을 수 없습니다.")
        
    dataclass = self.schemas[schema_name]
    table_name = self._to_snake_case(schema_name)
    
    field_names = [f.name for f in fields(dataclass)]
    
    columns_str = ", ".join(field_names)
    placeholders_str = ", ".join(["%s"] * len(field_names))
    
    update_columns = [f"{name} = EXCLUDED.{name}" for name in field_names if name != conflict_key]
    update_str = ",\n  ".join(update_columns)
    
    return (
      f"INSERT INTO {table_name} ({columns_str})\n"
      f"VALUES ({placeholders_str})\n"
      f"ON CONFLICT ({conflict_key}) DO UPDATE SET\n  {update_str},\n"
      f"  updated_at = CURRENT_TIMESTAMP;"
    )

# --- 사용 예시 ---
if __name__ == '__main__':
  # 프로젝트의 KIS_schemas 모듈을 import 합니다.
  # 이 파일의 위치에 따라 경로를 수정해야 할 수 있습니다.
  from src.data.schemas import KIS_schemas 

  # 1. SQLGenerator 인스턴스 생성 (모듈을 통째로 전달)
  sql_gen = SQLGenerator(KIS_schemas)

  # 2. 로드된 스키마 목록 확인
  print("\n--- 사용 가능한 스키마 목록 ---")
  available_schemas = sql_gen.get_available_schemas()
  print(available_schemas)

  # 3. 특정 스키마에 대한 SQL 생성
  print("\n--- KrStockBasicInfo CREATE SQL ---")
  # KrStockBasicInfo의 경우 'pdno'(상품번호)가 더 적합한 고유 키일 수 있습니다.
  create_sql_1 = sql_gen.generate_create_sql('KrStockBasicInfo', primary_key='pdno')
  print(create_sql_1)

  print("\n--- KrStockAskingPrice UPSERT SQL ---")
  upsert_sql_1 = sql_gen.generate_upsert_sql('KrStockAskingPrice', conflict_key='ticker')
  print(upsert_sql_1)
  
  print("\n--- KrStockIncomeStatement UPSERT SQL ---")
  # 손익계산서는 '종목코드'와 '결산년월' 복합 키가 필요하지만, 여기서는 'stac_yymm'을 예시로 사용
  # 이처럼 conflict_key를 유연하게 변경할 수 있습니다.
  upsert_sql_2 = sql_gen.generate_upsert_sql('KrStockIncomeStatement', conflict_key='stac_yymm')
  print(upsert_sql_2)