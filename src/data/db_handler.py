import os
from typing import List, Optional
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

class DBHandler:
  """
  데이터베이스 연결 및 모든 I/O 작업을 처리하는 클래스.

  SQLAlchemy 엔진을 사용하여 Pandas DataFrame과의 연동을 관리합니다.
  """
  def __init__(self, db_name: str = os.getenv("DATA_DB_NAME")):
    """DBHandler 인스턴스를 초기화합니다.

    .env 파일에서 환경 변수를 로드하여 SQLAlchemy 데이터베이스 엔진을 생성합니다.
    연결 정보가 누락된 경우, 엔진은 생성되지 않습니다.

    Args:
      db_name (str): 연결할 데이터베이스의 이름. 기본값은 'DATA_DB_NAME' 환경 변수입니다.
    
    Raises:
      ValueError: .env 파일에 데이터베이스 연결 정보가 누락된 경우 발생합니다.
    """
    load_dotenv()
    try:
      user=os.getenv("DATA_DB_USER")
      password=os.getenv("DATA_DB_PASSWORD")
      host='localhost'
      port=os.getenv("DATA_DB_PORT")
        
      if not all([user, password, host, port, db_name]):
        raise ValueError("데이터베이스 연결 정보가 .env 파일에 올바르게 설정되지 않았습니다.")

      conn_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
      self.engine = create_engine(conn_string)
      
    except Exception as e:
      print(f"❌ 데이터베이스 엔진 생성 실패: {e}")
      self.engine = None

  def _load_sql(self, file_path: str) -> str | None:
    """지정된 경로의 .sql 파일을 읽어 문자열로 반환합니다.

    Args:
      file_path (str): 읽어올 .sql 파일의 경로.

    Returns:
      str | None: 파일의 내용을 담은 문자열. 파일을 찾지 못한 경우 None을 반환합니다.
    """
    try:
      with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    except FileNotFoundError:
      print(f"❌ SQL 파일을 찾을 수 없습니다: {file_path}")
      return None
    
  def create_table(self, path: str):
    """.sql 파일에 정의된 DDL(데이터 정의어)을 실행하여 테이블을 생성합니다.

    SQL 스크립트 파일을 읽어 세미콜론(;)으로 구분된 여러 개의 DDL 문을 개별적으로 실행합니다.

    Args:
      path (str): 실행할 DDL이 포함된 .sql 파일의 경로.
    """
    if self.engine is None:
      print("❌ DB 엔진이 없어 DDL 실행을 건너뜁니다.")
      return

    sql_script = self._load_sql(path)
    if not sql_script:
      return
    
    # SQL 스크립트를 세미콜론(;) 기준으로 나누어 리스트로 만듭니다.
    statements = [s.strip() for s in sql_script.split(';') if s.strip()]
    
    try:
      with self.engine.connect() as conn:
        # 각 SQL 문을 순서대로 실행합니다.
        for stmt in statements:
          conn.execute(text(stmt))
        conn.commit()
    except Exception as e:
      print(f"❌ DDL 실행 중 에러 발생: {e}")

  def replace_table_from_df(self, df: pd.DataFrame, table_name: str):
    """
    DataFrame의 스키마를 기반으로 테이블을 동적으로 생성하고 데이터를 삽입합니다.
    
    기존에 같은 이름의 테이블이 있다면 삭제한 후, DataFrame의 DDL(Data Definition Language)에 맞춰
    새로운 테이블을 생성하고 모든 데이터를 삽입합니다.
    """
    if self.engine is None:
      print("❌ 데이터베이스 엔진이 없어 저장을 건너뜁니다.")
      return

    if df.empty:
      print(f"저장할 데이터가 없어 '{table_name}' 작업을 건너뜁니다.")
      return

    try:
      with self.engine.connect() as conn:
        # 1. 기존 테이블이 있다면 삭제 (CASCADE 옵션으로 의존성 있는 객체도 함께 삭제)
        conn.execute(text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;'))
        
        # 2. DataFrame 스키마를 기반으로 CREATE TABLE SQL 구문 생성
        #    pd.io.sql.get_schema 함수가 이 역할을 수행합니다.
        create_sql = pd.io.sql.get_schema(df, name=table_name, con=conn)
        
        # 3. 생성된 SQL을 실행하여 테이블 생성
        conn.execute(text(create_sql))
        conn.commit()
      
      # 4. 생성된 테이블에 데이터 삽입 (기존 save_df 메서드 재활용)
      self.save_df(df, table_name, if_exists='append')
      
    except Exception as e:
      print(f"❌ 동적 테이블 생성 및 데이터 저장 중 에러 발생: {e}")

  def insert_data(self, df: pd.DataFrame, path: str):
    """DataFrame의 데이터를 데이터베이스에 대량 삽입(Bulk Insert)합니다.

    .sql 파일에서 INSERT 문을 로드한 후, DBAPI의 'executemany'를 사용하여 
    Pandas DataFrame의 데이터를 효율적으로 삽입합니다.

    Args:
      df (pd.DataFrame): 데이터베이스에 삽입할 데이터가 담긴 DataFrame.
      path (str): 실행할 INSERT 문이 포함된 .sql 파일의 경로.
    """
    if self.engine is None:
      print("❌ DB 엔진이 없어 저장을 건너뜁니다.")
      return

    if df.empty:
      print("저장할 데이터가 없어 DB 저장을 건너뜁니다.")
      return
    
    insert_sql = self._load_sql(path)
    if not insert_sql: 
      return
    
    # SQLAlchemy 엔진에서 기본 DBAPI 연결(raw_connection)을 가져옵니다.
    conn = self.engine.raw_connection()
    try:
      with conn.cursor() as cursor:
        # DataFrame의 각 행을 튜플로 변환하여 리스트를 생성합니다.
        data_tuples = [tuple(row) for row in df.itertuples(index=False)]
        
        # executemany는 튜플의 리스트를 받아 대량 INSERT를 수행하는 데 최적화되어 있습니다.
        cursor.executemany(insert_sql, data_tuples)
          
      conn.commit()
      print(f"✅ 총 {len(data_tuples)}개 행 INSERT 성공!")
    except Exception as e:
      print(f"❌ INSERT 작업 중 에러 발생: {e}")
      conn.rollback()
    finally:
      conn.close()


  def get_latest_date(self, table_name: str, date_column: str, default_start_date: str) -> str:
    """특정 테이블의 날짜 컬럼에서 가장 최근 날짜를 조회합니다.

    테이블의 마지막 데이터 업데이트 시점을 확인하여, 데이터 수집 시작일을
    결정하는 데 사용됩니다. 테이블이나 데이터가 없으면 기본 시작일을 반환합니다.

    Args:
      table_name (str): 조회할 테이블의 이름.
      date_column (str): 날짜 정보가 들어있는 컬럼의 이름.
      default_start_date (str): 테이블이나 데이터가 없을 때 반환할 기본 시작 날짜. (YYYYMMDD 형식)

    Returns:
      str: 조회된 가장 최근 날짜의 다음 날짜, 또는 기본 시작 날짜.
        (YYYYMMDD 형식)
    """
    if self.engine is None:
      #print("DB 엔진이 없어 기본 시작일을 반환합니다.")
      return default_start_date
        
    try:
      with self.engine.connect() as conn:
        query_exists = text(f"SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = '{table_name}');")
        if not conn.execute(query_exists).scalar():
          #print(f"'{table_name}' 테이블이 없어 기본 시작일({default_start_date})부터 수집합니다.")
          return default_start_date

        query = text(f'SELECT MAX("{date_column}") FROM {table_name};')
        result = conn.execute(query).scalar()
      
      if result is None:
        #print(f"'{table_name}' 테이블에 데이터가 없어 기본 시작일({default_start_date})부터 수집합니다.")
        return default_start_date
      else:
        latest_date = datetime.strptime(str(result), "%Y%m%d")
        start_date = (latest_date + timedelta(days=1)).strftime("%Y%m%d")
        #print(f"'{table_name}'의 최근 데이터 날짜는 {latest_date.strftime('%Y%m%d')} 입니다. {start_date}부터 수집을 시작합니다.")
        return start_date

    except Exception as e:
      print(f"⚠️ DB 최근 날짜 조회 중 오류: {e}. 기본 시작일({default_start_date})부터 수집합니다.")
      return default_start_date


  def save_df(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append'):
    """Pandas DataFrame을 PostgreSQL 테이블에 저장합니다.

    Pandas에 내장된 'to_sql' 메서드를 사용하여 DataFrame을 데이터베이스 테이블로
    직접 저장합니다.

    Args:
      df (pd.DataFrame): 저장할 데이터가 담긴 DataFrame.
      table_name (str): 데이터를 저장할 테이블의 이름.
      if_exists (str): 테이블이 이미 존재할 경우의 동작을 지정합니다.
        {'fail', 'replace', 'append'}, 기본값: 'append'.
    """
    if self.engine is None:
      print("❌ 데이터베이스 엔진이 없어 저장을 건너뜁니다.")
      return

    if df.empty:
      # print(f"저장할 데이터가 없어 '{table_name}' 작업을 건너뜁니다.")
      return

    try:
      df.to_sql(
        table_name,
        con=self.engine,
        if_exists=if_exists,
        index=False,
        chunksize=10000,  # 데이터를 10,000행씩 나누어 저장
        method='multi'    # 여러 행을 하나의 INSERT 구문으로 묶어 속도 향상
      )
    except Exception as e:
      print(f"❌ 데이터베이스 저장 중 에러 발생: {e}")

  def fetch_data(self, table_name: str, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    지정된 테이블에서 데이터를 조회합니다.

    'columns' 파라미터가 제공되면 해당 컬럼들만 조회하고,
    제공되지 않으면 테이블의 모든 컬럼(`*`)을 조회합니다.

    Args:
      table_name (str): 데이터를 조회할 테이블의 이름.
      columns (Optional[List[str]], optional): 조회할 컬럼 이름들의 리스트.
        기본값은 None이며, 이 경우 모든 컬럼을 조회합니다.

    Returns:
      pd.DataFrame: 조회된 데이터를 담은 DataFrame. 오류 발생 시 빈 DataFrame을 반환합니다.
    """
    if self.engine is None:
      print("❌ 데이터베이스 엔진이 없어 조회를 건너뜁니다.")
      return pd.DataFrame()

    # 'columns' 파라미터 유무에 따라 SQL 쿼리를 동적으로 생성합니다.
    if columns:
      # 특정 컬럼이 지정된 경우
      column_str = ", ".join([f'"{col}"' for col in columns])
      query = f"SELECT {column_str} FROM {table_name};"
    else:
      # 'columns'가 None이거나 비어있는 경우, 모든 컬럼을 조회
      query = f"SELECT * FROM {table_name};"

    try:
      df = pd.read_sql_query(sql=query, con=self.engine)
      return df
    except Exception as e:
      print(f"❌ '{table_name}' 테이블 조회 중 에러 발생: {e}")
      return pd.DataFrame()