# connect_local.py

import psycopg2
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv(".env")

def connect_to_local_db():
  try:
    conn = psycopg2.connect(
      dbname=os.getenv("DATA_DB_NAME"),
      user=os.getenv("DATA_DB_USER"),
      password=os.getenv("DATA_DB_PASSWORD"),
      host="localhost",
      port=os.getenv("DATA_DB_PORT")
    )
    print("✅ 로컬 DB 연결 성공")
    conn.close()
  except Exception as e:
    print("❌ 로컬 DB 연결 실패:", e)

if __name__ == "__main__":
  connect_to_local_db()
