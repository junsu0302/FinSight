from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
from dataclasses import fields
from tqdm import tqdm
import pandas as pd

from src.hooks.KIS_API_hook import KISAPIHook
from src.utils.get_asset_list import get_asset_list
from src.data.schemas.KIS_schemas import KrStockBasicInfo, KrStockBalanceSheet, KrStockFinancialRatio, KrStockGrowthRatio, KrStockIncomeStatement, KrStockOtherMajorRatio, KrStockProfitRatio, KrStockStabilityRatio, KrStockDividend, KrStockEstimatePerform, KrStockInvestOpinion, KrStockInvestOpbysec, KrStockPriceBasic, KrStockPriceDetail, KrStockAskingPrice, KrStockInvestor, KrStockMember, KrStockDailyItemchartprice
from src.data.db_handler import DBHandler
from src.etl.transformer.KIS_transformer import KISTransformer

# ----- [국내 주식 정보] CONFIG 정의 -----
KR_STOCK_BASIC_INFO_CONFIG = {
  "description": "한국 주식 종목 기본 정보", "schemas": KrStockBasicInfo,
  "asset": "kr_stock", "path": "basic_info", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_BALANCE_SHEET_CONFIG = {
  "description": "국내 주식 대차대조표", "schemas": KrStockBalanceSheet,
  "asset": "kr_stock", "path": "balance_sheet", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_INCOME_STATEMENT_CONFIG = {
  "description": "국내 주식 손익계산서", "schemas": KrStockIncomeStatement,
  "asset": "kr_stock", "path": "income_statement", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_FINANCIAL_RATIO_CONFIG = {
  "description": "국내 주식 재무 비율", "schemas": KrStockFinancialRatio,
  "asset": "kr_stock", "path": "financial_ratio", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_PROFIT_RATIO_CONFIG = {
  "description": "국내 주식 수익성비율", "schemas": KrStockProfitRatio,
  "asset": "kr_stock", "path": "profit_ratio", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_OTHER_MAJOR_RATIO_CONFIG = {
  "description": "국내 주식 기타 주요 비율", "schemas": KrStockOtherMajorRatio,
  "asset": "kr_stock", "path": "other_major_ratio", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_STABILITY_RATIO_CONFIG = {
  "description": "국내 주식 안정성 비율", "schemas": KrStockStabilityRatio,
  "asset": "kr_stock", "path": "stability_ratio", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_GROWTH_RATIO_CONFIG = {
  "description": "국내 주식 성장성 비율", "schemas": KrStockGrowthRatio,
  "asset": "kr_stock", "path": "growth_ratio", "table_type": "stock_info",
  "params": { "stock_code": "{ticker}" }
  
}

KR_STOCK_DIVIDEND_CONFIG = {
  "description": "국내 주식 배당일정", "schemas": KrStockDividend,
  "asset": "kr_stock", "path": "dividend", "table_type": "stock_info",
  "date_column": "record_date", "default_start_date": "20040101",
  "params": { "start_date": "{start_date}", "end_date": "{end_date}", "stock_code": "{ticker}" },
}

KR_STOCK_ESTIMATE_PERFORM_CONFIG = {
  "description": "국내 주식 종목추정실적", "schemas": KrStockEstimatePerform,
  "asset": "kr_stock", "path": "estimate_perform", "table_type": "stock_info",
  "transformer_name": "estimate_perform",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_INVEST_OPINION_CONFIG = {
  "description": "국내 주식 종목 투자 의견", "schemas": KrStockInvestOpinion,
  "asset": "kr_stock", "path": "invest_opinion", "table_type": "stock_info",
  "date_column": "stck_bsop_date", "default_start_date": "20040101",
  "params": { "stock_code": "{ticker}" , "start_date": "{start_date}", "end_date": "{end_date}" }
}

KR_STOCK_INVEST_OPBYSEC_CONFIG = {
  "description": "국내 주식 증권사별 투자의견", "schemas": KrStockInvestOpbysec,
  "asset": "kr_stock", "path": "invest_opbysec", "table_type": "stock_info",
  "date_column": "stck_bsop_date", "default_start_date": "20040101",
  "params": { "stock_code": "{ticker}" , "start_date": "{start_date}", "end_date": "{end_date}" }
}

# ----- [국내 주식 시세] CONFIG 정의 -----

KR_STOCK_PRICE_BASIC = {
  "description": "한국 주식 시세 기본 정보", "schemas": KrStockPriceBasic,
  "asset": "kr_stock", "path": "price_basic", "table_type": "stock_price",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_PRICE_DETAIL = {
  "description": "한국 주식 시세 세부 정보", "schemas": KrStockPriceDetail,
  "asset": "kr_stock", "path": "price_detail", "table_type": "stock_price",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_ASKING_PRICE = {
  "description": "한국 주식 호가/예상체결", "schemas": KrStockAskingPrice,
  "asset": "kr_stock", "path": "asking_price", "table_type": "stock_price",
  "transformer_name": "asking_price",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_INVESTOR = {
  "description": "한국 주식 투자자 정보", "schemas": KrStockInvestor,
  "asset": "kr_stock", "path": "investor", "table_type": "stock_price",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_MEMBER = {
  "description": "한국 주식 회원사 정보", "schemas": KrStockMember,
  "asset": "kr_stock", "path": "member", "table_type": "stock_price",
  "params": { "stock_code": "{ticker}" }
}

KR_STOCK_DAILY_ITEMCHARTPRICE = {
  "description": "한국 주식 기간별 시세", "schemas": KrStockDailyItemchartprice,
  "asset": "kr_stock", "path": "daily_itemchartprice", "table_type": "stock_price",
  "transformer_name": "daily_itemchartprice",
  "date_column": "stck_bsop_date", "default_start_date": "20040101",
  "params": { "stock_code": "{ticker}" , "start_date": "{start_date}", "end_date": "{end_date}" }
}


load_dotenv()

def generate_date_chunks(start_date_str, end_date_str, years_per_chunk=1):
  if not start_date_str or not end_date_str: return [(None, None)]
  start_date = datetime.strptime(start_date_str, "%Y%m%d")
  end_date = datetime.strptime(end_date_str, "%Y%m%d")
  chunks = []
  current_start = start_date
  while current_start <= end_date:
    current_end = current_start + timedelta(days=365 * years_per_chunk - 1)
    if current_end > end_date:
      current_end = end_date
    chunks.append((current_start.strftime("%Y%m%d"), current_end.strftime("%Y%m%d")))
    current_start = current_end + timedelta(days=1)
  return chunks

def KIS_collector(config: dict):
  desc = config["description"]
  asset, path, table_type = config["asset"], config["path"], config["table_type"]
  params_template = config.get("params", {})
  table_name = f"{config['asset']}_{config['path']}"

  kis_hook, db_handler, transformer = KISAPIHook(), DBHandler(db_name="data_lake"), KISTransformer()
  create_sql_path = f"./sql/{asset}/data_lake/{table_type}/ddl/create_{table_name}.sql"
  insert_sql_path = f"./sql/{asset}/data_lake/{table_type}/dml/insert_{table_name}.sql"
  
  tickers=["005930","091990","105560","035420","373220","016360","207940","247540","017670","139480","004020","352820"] # Test Tickers
  #tickers = get_asset_list(config["asset"])
  
  db_handler.create_table(create_sql_path)

  date_chunks = [(None, None)]
  if config.get("date_column"):
    start_date = db_handler.get_latest_date(
      table_name=table_name, date_column=config["date_column"],
      default_start_date=config["default_start_date"]
    )
    end_date = datetime.today().strftime('%Y%m%d')
    if start_date > end_date:
      print(f"✅ 모든 데이터가 최신 상태입니다. 수집을 종료합니다."); return
    date_chunks = generate_date_chunks(start_date, end_date, config.get("chunk_years", 1))

  all_raw_results = []
  for ticker in tqdm(tickers, desc=desc):
    for start_chunk, end_chunk in date_chunks:
      try:
        api_function = getattr(kis_hook, f"get_{asset}_{path}")
        dynamic_params = {}
        for key, value in params_template.items():
          temp_value = value
          if "{ticker}" in temp_value: temp_value = temp_value.replace("{ticker}", ticker)
          if "{start_date}" in temp_value and start_chunk: temp_value = temp_value.replace("{start_date}", start_chunk)
          if "{end_date}" in temp_value and end_chunk: temp_value = temp_value.replace("{end_date}", end_chunk)
          dynamic_params[key] = temp_value
        
        api_response = api_function(**dynamic_params)
        if not api_response: continue

        if isinstance(api_response, dict): api_response = [api_response]
        for item in api_response:
          item['ticker'] = ticker
        all_raw_results.extend(api_response)
      
      except Exception as e:
        tqdm.write(f"⚠️ '{ticker}' 처리 중 오류: {e}")
      time.sleep(0.2)
  
  if not all_raw_results:
    print("수집된 데이터가 없습니다."); return

  raw_df = pd.DataFrame(all_raw_results)
  transformer_name = config.get("transformer_name")
  
  if transformer_name:
    final_df = transformer.transform(transformer_name=transformer_name, raw_df=raw_df)
  else:
    final_df = raw_df
  
  if not final_df.empty and config.get("schemas"):
    schema_columns = [field.name for field in fields(config["schemas"])]

    sql_column_order = ['ticker'] + [col for col in schema_columns if col != 'ticker']

    final_df = final_df.reindex(columns=sql_column_order)
      
  db_handler.insert_data(final_df, insert_sql_path)


if __name__ == "__main__":
  # ----- [국내 주식 정보] Collector -----
  # KIS_collector(KR_STOCK_BASIC_INFO_CONFIG)
  # KIS_collector(KR_STOCK_BALANCE_SHEET_CONFIG)
  # KIS_collector(KR_STOCK_INCOME_STATEMENT_CONFIG)
  # KIS_collector(KR_STOCK_FINANCIAL_RATIO_CONFIG)
  # KIS_collector(KR_STOCK_PROFIT_RATIO_CONFIG)
  # KIS_collector(KR_STOCK_OTHER_MAJOR_RATIO_CONFIG)
  # KIS_collector(KR_STOCK_STABILITY_RATIO_CONFIG)
  # KIS_collector(KR_STOCK_GROWTH_RATIO_CONFIG)
  # KIS_collector(KR_STOCK_DIVIDEND_CONFIG)
  # KIS_collector(KR_STOCK_ESTIMATE_PERFORM_CONFIG)
  # KIS_collector(KR_STOCK_INVEST_OPINION_CONFIG)
  # KIS_collector(KR_STOCK_INVEST_OPBYSEC_CONFIG)

  # ----- [국내 주식 시세] Collector -----
  # KIS_collector(KR_STOCK_PRICE_BASIC)
  # KIS_collector(KR_STOCK_PRICE_DETAIL)
  # KIS_collector(KR_STOCK_ASKING_PRICE)
  # KIS_collector(KR_STOCK_INVESTOR)
  # KIS_collector(KR_STOCK_MEMBER)
  KIS_collector(KR_STOCK_DAILY_ITEMCHARTPRICE)