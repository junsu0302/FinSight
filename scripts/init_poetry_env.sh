#!/bin/bash

set -e

PROJECT_NAME=${1:-"finsight"}

echo "Poetry 프로젝트 초기화: ${PROJECT_NAME}"
poetry init --name "$PROJECT_NAME" --no-interaction --dev-dependency black

echo "가상환경 로컬에 생성 설정"
poetry config virtualenvs.in-project true --local
poetry config virtualenvs.create true --local

echo "의존성 설치"
poetry install --no-root

echo "완료: 프로젝트 디렉토리 내 '.venv' 생성 및 독립 가상환경 구축"
