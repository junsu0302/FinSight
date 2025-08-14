-- kr_stock_stability_ratio 테이블에 데이터를 삽입하거나,
-- (ticker, stac_yymm)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_stability_ratio (
  ticker,
  stac_yymm,
  lblt_rate,
  bram_depn,
  crnt_rate,
  quck_rate
) VALUES (
  %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stac_yymm) DO UPDATE SET
  lblt_rate = EXCLUDED.lblt_rate,
  bram_depn = EXCLUDED.bram_depn,
  crnt_rate = EXCLUDED.crnt_rate,
  quck_rate = EXCLUDED.quck_rate,
  updated_at = CURRENT_TIMESTAMP;