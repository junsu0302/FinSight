-- 유저가 존재하지 않으면 생성
DO
$$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_catalog.pg_roles WHERE rolname = 'user'
  ) THEN
    CREATE ROLE "user" WITH LOGIN PASSWORD 'password';
  END IF;
END
$$;

-- 데이터베이스가 존재하지 않으면 생성
DO
$$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_database WHERE datname = 'finsight'
  ) THEN
    CREATE DATABASE finsight OWNER "user";
  END IF;
END
$$;

-- 권한 부여 (데이터베이스가 이미 존재하는 경우에도 문제 없음)
GRANT ALL PRIVILEGES ON DATABASE finsight TO "user";
