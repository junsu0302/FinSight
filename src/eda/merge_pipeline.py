import sys
from dotenv import load_dotenv
from pathlib import Path
import yaml
import pandas as pd
# 제공해주신 eda_pipeline.py를 참고하여 DB 핸들러 경로를 가정합니다.
from src.data.db_handler import DBHandler
# 제공해주신 tasks.py의 ColumnSelector를 import합니다.
from tasks import ColumnSelector

def run_merge_pipeline(config_path: str):
  """
  YAML 설정 파일을 기반으로 테이블별 컬럼 선택 후 순차적으로 병합합니다.
  """
  # 1. 설정 파일 로드
  with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

  db_handler = DBHandler(db_name="data_warehouse")
  processed_dfs = {}

  # 2. 각 테이블을 로드하고 명시된 컬럼만 선택
  print("--- Step 1: Selecting columns from tables ---")
  for alias, table_info in config['source_tables'].items():
    table_name = table_info['table_name']
    columns_to_keep = table_info['columns']

    print(f"Loading '{table_name}'...")
    df = db_handler.fetch_data(table_name)

    # 제공된 tasks.py의 ColumnSelector 사용
    selector = ColumnSelector(columns_to_keep=columns_to_keep)
    processed_df = selector.execute(df, verbose=False)
    processed_dfs[alias] = processed_df
    print(f"Selected {len(columns_to_keep)} columns from '{table_name}'.")

  # 3. `merge_strategy`에 따라 테이블 결합
  print("\n--- Step 2: Merging tables ---")
  strategy = config['merge_strategy']
  base_table_alias = strategy['base_table']
  join_key = strategy['join_key']
  join_how = strategy['join_how']

  # 기준이 되는 DataFrame으로 초기화
  merged_df = processed_dfs[base_table_alias]
  print(f"Base table: '{base_table_alias}', initial shape: {merged_df.shape}")

  # 순서대로 병합 수행
  for target_alias in strategy['merge_sequence']:
    print(f"Merging with '{target_alias}'...")
    merged_df = pd.merge(
      merged_df,
      processed_dfs[target_alias],
      on=join_key,
      how=join_how
    )
    print(f"  -> Current shape after merge: {merged_df.shape}")

    # 4. 최종 결과를 DB에 저장
    final_table_name = config['final_table_name']
    db_handler.replace_table_from_df(df=merged_df, table_name=final_table_name)
    print(f"\n✅ Success! Saved to '{final_table_name}'. Final shape: {merged_df.shape}")


if __name__ == "__main__":
  current_dir = Path(__file__).parent
  project_root = current_dir.parent.parent
  env_path = project_root / '.env'

  load_dotenv(dotenv_path=env_path)
  if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
  
  # 설정 파일 경로 지정
  #config_path = current_dir / 'configs' / f'kr_stock_static_data.yml'
  config_path = current_dir / 'configs' / f'kr_stock_quartely_data.yml'
  
  run_merge_pipeline(config_path)