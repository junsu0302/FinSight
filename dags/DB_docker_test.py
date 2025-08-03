# connect_docker.py

import psycopg2
import os

def connect_to_docker_db():
  try:
    conn = psycopg2.connect(
      dbname=os.getenv("DATA_DB_NAME"),
      user=os.getenv("DATA_DB_USER"),
      password=os.getenv("DATA_DB_PASSWORD"),
      host=os.getenv("DATA_DB_HOST"),   # docker-compose에서 지정한 서비스명
      port=os.getenv("POSTGRES_PORT")
    )
    print("✅ Docker 내부에서 DB 연결 성공")
    conn.close()
  except Exception as e:
    print("❌ Docker DB 연결 실패:", e)

if __name__ == "__main__":
  connect_to_docker_db()
