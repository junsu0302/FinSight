-- kr_stock_balance_sheet 테이블에 데이터를 삽입하거나,
-- (ticker, stac_yymm)이 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)

INSERT INTO kr_stock_income_statement (
  ticker,
  stac_yymm,
  sale_account,
  sale_cost,
  sale_totl_prfi,
  depr_cost,
  sell_mang,
  bsop_prti,
  bsop_non_ernn,
  bsop_non_expn,
  op_prfi,
  spec_prfi,
  spec_loss,
  thtr_ntin
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, stac_yymm) DO UPDATE SET
  sale_account = EXCLUDED.sale_account,
  sale_cost = EXCLUDED.sale_cost,
  sale_totl_prfi = EXCLUDED.sale_totl_prfi,
  depr_cost = EXCLUDED.depr_cost,
  sell_mang = EXCLUDED.sell_mang,
  bsop_prti = EXCLUDED.bsop_prti,
  bsop_non_ernn = EXCLUDED.bsop_non_ernn,
  bsop_non_expn = EXCLUDED.bsop_non_expn,
  op_prfi = EXCLUDED.op_prfi,
  spec_prfi = EXCLUDED.spec_prfi,
  spec_loss = EXCLUDED.spec_loss,
  thtr_ntin = EXCLUDED.thtr_ntin,
  updated_at = CURRENT_TIMESTAMP;