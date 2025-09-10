-- kr_stock_growth_ratio 테이블에 데이터를 삽입하거나,
-- (ticker, stac_yymm)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_growth_ratio (
  ticker,
  stac_yymm,
  grs,
  bsop_prfi_inrt,
  equt_inrt,
  totl_aset_inrt
) VALUES (
  %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stac_yymm) DO UPDATE SET
  grs = EXCLUDED.grs,
  bsop_prfi_inrt = EXCLUDED.bsop_prfi_inrt,
  equt_inrt = EXCLUDED.equt_inrt,
  totl_aset_inrt = EXCLUDED.totl_aset_inrt,
  updated_at = CURRENT_TIMESTAMP;