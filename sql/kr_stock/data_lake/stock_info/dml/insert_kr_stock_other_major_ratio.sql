-- kr_stock_other_major_ratio 테이블에 데이터를 삽입하거나,
-- (ticker, stac_yymm)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_other_major_ratio (
  ticker,
  stac_yymm,
  payout_rate,
  eva,
  ebitda,
  ev_ebitda
) VALUES (
  %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stac_yymm) DO UPDATE SET
  payout_rate = EXCLUDED.payout_rate,
  eva = EXCLUDED.eva,
  ebitda = EXCLUDED.ebitda,
  ev_ebitda = EXCLUDED.ev_ebitda,
  updated_at = CURRENT_TIMESTAMP;