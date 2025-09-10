import os
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
    """
    DBHandler 인스턴스를 초기화하고 데이터베이스 엔진을 생성합니다.
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
    """지정된 경로의 .sql 파일을 읽어서 문자열로 반환합니다."""
    try:
      with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    except FileNotFoundError:
      print(f"❌ SQL 파일을 찾을 수 없습니다: {file_path}")
      return None
    
  def create_table(self, path: str):
    """
    [수정] .sql 파일 안의 여러 SQL문(;)을 개별적으로 실행합니다.
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

  def insert_data(self, df: pd.DataFrame, path: str):
    """
    [수정] DBAPI의 cursor.executemany를 사용하여 튜플 리스트를 효율적으로 삽입합니다.
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
    """
    지정된 테이블에서 가장 최근 날짜를 조회하여, 그 다음날을 반환합니다.
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
    """DataFrame을 PostgreSQL에 저장합니다."""
    if self.engine is None:
      print("❌ 데이터베이스 엔진이 없어 저장을 건너뜁니다.")
      return

    if df.empty:
      # print(f"저장할 데이터가 없어 '{table_name}' 작업을 건너뜁니다.")
      return

    try:
      df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)
    except Exception as e:
      print(f"❌ 데이터베이스 저장 중 에러 발생: {e}")