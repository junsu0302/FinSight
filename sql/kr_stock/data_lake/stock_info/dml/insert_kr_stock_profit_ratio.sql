-- kr_stock_profit_ratio 테이블에 데이터를 삽입하거나,
-- (ticker, stac_yymm)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_profit_ratio (
  ticker,
  stac_yymm,
  cptl_ntin_rate,
  self_cptl_ntin_inrt,
  sale_ntin_rate,
  sale_totl_rate
) VALUES (
  %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stac_yymm) DO UPDATE SET
  cptl_ntin_rate = EXCLUDED.cptl_ntin_rate,
  self_cptl_ntin_inrt = EXCLUDED.self_cptl_ntin_inrt,
  sale_ntin_rate = EXCLUDED.sale_ntin_rate,
  sale_totl_rate = EXCLUDED.sale_totl_rate,
  updated_at = CURRENT_TIMESTAMP;