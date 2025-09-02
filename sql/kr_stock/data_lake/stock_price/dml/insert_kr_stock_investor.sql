-- kr_stock_investor 테이블에 데이터를 삽입하거나,
-- (ticker, stck_bsop_date)가 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_investor (
  ticker, stck_bsop_date, stck_clpr, prdy_vrss, prdy_vrss_sign, prsn_ntby_qty, frgn_ntby_qty,
  orgn_ntby_qty, prsn_ntby_tr_pbmn, frgn_ntby_tr_pbmn, orgn_ntby_tr_pbmn, prsn_shnu_vol,
  frgn_shnu_vol, orgn_shnu_vol, prsn_shnu_tr_pbmn, frgn_shnu_tr_pbmn, orgn_shnu_tr_pbmn,
  prsn_seln_vol, frgn_seln_vol, orgn_seln_vol, prsn_seln_tr_pbmn, frgn_seln_tr_pbmn,
  orgn_seln_tr_pbmn
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stck_bsop_date) DO UPDATE SET
  stck_clpr = EXCLUDED.stck_clpr,
  prdy_vrss = EXCLUDED.prdy_vrss,
  prdy_vrss_sign = EXCLUDED.prdy_vrss_sign,
  prsn_ntby_qty = EXCLUDED.prsn_ntby_qty,
  frgn_ntby_qty = EXCLUDED.frgn_ntby_qty,
  orgn_ntby_qty = EXCLUDED.orgn_ntby_qty,
  prsn_ntby_tr_pbmn = EXCLUDED.prsn_ntby_tr_pbmn,
  frgn_ntby_tr_pbmn = EXcluded.frgn_ntby_tr_pbmn,
  orgn_ntby_tr_pbmn = EXCLUDED.orgn_ntby_tr_pbmn,
  prsn_shnu_vol = EXCLUDED.prsn_shnu_vol,
  frgn_shnu_vol = EXCLUDED.frgn_shnu_vol,
  orgn_shnu_vol = EXCLUDED.orgn_shnu_vol,
  prsn_shnu_tr_pbmn = EXCLUDED.prsn_shnu_tr_pbmn,
  frgn_shnu_tr_pbmn = EXCLUDED.frgn_shnu_tr_pbmn,
  orgn_shnu_tr_pbmn = EXCLUDED.orgn_shnu_tr_pbmn,
  prsn_seln_vol = EXCLUDED.prsn_seln_vol,
  frgn_seln_vol = EXCLUDED.frgn_seln_vol,
  orgn_seln_vol = EXCLUDED.orgn_seln_vol,
  prsn_seln_tr_pbmn = EXCLUDED.prsn_seln_tr_pbmn,
  frgn_seln_tr_pbmn = EXCLUDED.frgn_seln_tr_pbmn,
  orgn_seln_tr_pbmn = EXCLUDED.orgn_seln_tr_pbmn,
  updated_at = CURRENT_TIMESTAMP;