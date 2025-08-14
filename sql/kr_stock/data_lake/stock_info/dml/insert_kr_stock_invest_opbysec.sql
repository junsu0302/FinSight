-- kr_stock_invest_opbysec 테이블에 데이터를 삽입하거나,
-- (stck_shrn_iscd, stck_bsop_date, mbcr_name)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_invest_opbysec (
  ticker, stck_bsop_date, stck_shrn_iscd, hts_kor_isnm, invt_opnn, invt_opnn_cls_code,
  rgbf_invt_opnn, rgbf_invt_opnn_cls_code, mbcr_name, stck_prpr, prdy_vrss,
  prdy_vrss_sign, prdy_ctrt, hts_goal_prc, stck_prdy_clpr, stft_esdg, dprt
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (stck_shrn_iscd, stck_bsop_date, mbcr_name) DO UPDATE SET
  hts_kor_isnm = EXCLUDED.hts_kor_isnm,
  invt_opnn = EXCLUDED.invt_opnn,
  invt_opnn_cls_code = EXCLUDED.invt_opnn_cls_code,
  rgbf_invt_opnn = EXCLUDED.rgbf_invt_opnn,
  rgbf_invt_opnn_cls_code = EXCLUDED.rgbf_invt_opnn_cls_code,
  stck_prpr = EXCLUDED.stck_prpr,
  prdy_vrss = EXCLUDED.prdy_vrss,
  prdy_vrss_sign = EXCLUDED.prdy_vrss_sign,
  prdy_ctrt = EXCLUDED.prdy_ctrt,
  hts_goal_prc = EXCLUDED.hts_goal_prc,
  stck_prdy_clpr = EXCLUDED.stck_prdy_clpr,
  stft_esdg = EXCLUDED.stft_esdg,
  dprt = EXCLUDED.dprt,
  updated_at = CURRENT_TIMESTAMP;