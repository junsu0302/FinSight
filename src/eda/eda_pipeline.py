from dotenv import load_dotenv
from pathlib import Path
import sys
import yaml
from preprocessor import DataFramePreprocessor
from src.data.db_handler import DBHandler
from tasks import (
    MissingValueCleaner,
    NullColumnRemover,
    ConstantColumnRemover,
    ColumnSelector,
    AutomaticTypeConverter,
    ManualTypeConverter
)

def run_pipeline(config_path: str, verbose:bool=False):
  # 1. 설정 파일 로드
  with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
  
  table_name = config['table_name']
  
  # 2. 데이터 로드
  db_handler = DBHandler(db_name="data_lake")
  raw_df = db_handler.fetch_data(table_name=table_name)

  # 3. 설정 파일 기반으로 파이프라인 구성 및 실행
  preprocessor = DataFramePreprocessor(df=raw_df, verbose=verbose)

  processed_df = (
    preprocessor
    .add_task(MissingValueCleaner(values_to_replace=config['auto_cleaning_rules']['replace_as_null']))
    .add_task(NullColumnRemover(threshold=config['auto_cleaning_rules']['drop_nulls_threshold']))
    .add_task(ConstantColumnRemover(threshold=config['auto_cleaning_rules']['drop_unique_threshold']))
    .add_task(ColumnSelector(columns_to_keep=config['manual_column_selection']))
    .add_task(AutomaticTypeConverter(
      category_ratio=config['auto_dtype_rules']['category_ratio'],
      date_success_rate=config['auto_dtype_rules']['date_success_rate']
    ))
    .add_task(ManualTypeConverter(dtype_map=config['manual_dtype_map']))
    .process()
  )
  
  if not processed_df.empty:
    dwh_handler = DBHandler(db_name="data_warehouse")
    dwh_handler.replace_table_from_df(df=processed_df, table_name=table_name)

  raw_count = len(raw_df.columns)
  processed_count = len(processed_df.columns)
  print(
    f"✅ Success EDA pipeline for {table_name:<30} | "
    f"[raw: {raw_count:>2} cols] -> [processed: {processed_count:>2} cols]"
  )
  return processed_df

if __name__ == "__main__":
  current_dir = Path(__file__).parent
  project_root = current_dir.parent.parent
  env_path = project_root / '.env'

  load_dotenv(dotenv_path=env_path)
  if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

  # Data Lake : KIS API [종목정보] >> Data Warehouse
  for path in ["basic_info", "balance_sheet", "dividend", "growth_ratio", "financial_ratio", "estimate_perform", "income_statement", "stability_ratio", "profit_ratio", "other_major_ratio"]:
    config_path = current_dir / 'configs/stock_info' / f'kr_stock_{path}.yml'
    run_pipeline(config_path, verbose=False)

  # Data Lake : KIS API [기본시세] >> Data Warehouse
  for path in ["asking_price", "price_basic", "price_detail", "daily_itemchartprice"]:
    config_path = current_dir / 'configs/stock_price' / f'kr_stock_{path}.yml'
    run_pipeline(config_path, verbose=False)