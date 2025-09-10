-- kr_stock_invest_opinion 테이블에 데이터를 삽입하거나, 
-- (ticker, stck_bsop_date, mbcr_name)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)
INSERT INTO kr_stock_invest_opinion (
  ticker, stck_bsop_date, mbcr_name, invt_opnn, invt_opnn_cls_code, 
  rgbf_invt_opnn, rgbf_invt_opnn_cls_code, hts_goal_prc, stck_prdy_clpr, 
  stck_nday_esdg, nday_dprt, stft_esdg, dprt
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stck_bsop_date, mbcr_name) DO UPDATE SET
  invt_opnn = EXCLUDED.invt_opnn,
  invt_opnn_cls_code = EXCLUDED.invt_opnn_cls_code,
  rgbf_invt_opnn = EXCLUDED.rgbf_invt_opnn,
  rgbf_invt_opnn_cls_code = EXCLUDED.rgbf_invt_opnn_cls_code,
  hts_goal_prc = EXCLUDED.hts_goal_prc,
  stck_prdy_clpr = EXCLUDED.stck_prdy_clpr,
  stck_nday_esdg = EXCLUDED.stck_nday_esdg,
  nday_dprt = EXCLUDED.nday_dprt,
  stft_esdg = EXCLUDED.stft_esdg,
  dprt = EXCLUDED.dprt,
  updated_at = CURRENT_TIMESTAMP;