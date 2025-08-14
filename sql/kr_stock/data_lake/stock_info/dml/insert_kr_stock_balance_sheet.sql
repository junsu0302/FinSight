-- kr_stock_balance_sheet 테이블에 데이터를 삽입하거나,
-- (ticker, stac_yymm)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_balance_sheet (
  ticker,
  stac_yymm,
  cras,
  fxas,
  total_aset,
  flow_lblt,
  fix_lblt,
  total_lblt,
  cpfn,
  cfp_surp,
  prfi_surp,
  total_cptl
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stac_yymm) DO UPDATE SET
  cras = EXCLUDED.cras,
  fxas = EXCLUDED.fxas,
  total_aset = EXCLUDED.total_aset,
  flow_lblt = EXCLUDED.flow_lblt,
  fix_lblt = EXCLUDED.fix_lblt,
  total_lblt = EXCLUDED.total_lblt,
  cpfn = EXCLUDED.cpfn,
  cfp_surp = EXCLUDED.cfp_surp,
  prfi_surp = EXCLUDED.prfi_surp,
  total_cptl = EXCLUDED.total_cptl,
  updated_at = CURRENT_TIMESTAMP;