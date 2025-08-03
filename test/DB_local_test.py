# test_db_connection.py
# utils/env_detect.py

import os

def is_docker():
  # Docker 컨테이너에서는 이 경로가 존재함
  return os.path.exists('/.dockerenv')
# 환경에 따라 다른 DB 연결 함수 import
if is_docker():
  from data.connect_docker import connect_to_docker_db as connect
  print("Docker 환경에서 DB 연결 테스트 수행 중...")
else:
  from data.connect_local import connect_to_local_db as connect
  print("로컬 환경에서 DB 연결 테스트 수행 중...")

# 연결 테스트 실행
connect()
