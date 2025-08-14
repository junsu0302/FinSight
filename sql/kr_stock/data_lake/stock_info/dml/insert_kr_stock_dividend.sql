-- kr_stock_dividend 테이블에 데이터를 삽입하거나, 
-- (sht_cd, record_date, divi_kind)가 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)
INSERT INTO kr_stock_dividend (
  sht_cd, record_date, divi_kind, ticker, isin_name, face_val, 
  per_sto_divi_amt, divi_rate, stk_divi_rate, divi_pay_dt, stk_div_pay_dt, 
  odd_pay_dt, stk_kind, high_divi_gb
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (sht_cd, record_date, divi_kind) DO UPDATE SET
  ticker = EXCLUDED.ticker,
  isin_name = EXCLUDED.isin_name,
  face_val = EXCLUDED.face_val,
  per_sto_divi_amt = EXCLUDED.per_sto_divi_amt,
  divi_rate = EXCLUDED.divi_rate,
  stk_divi_rate = EXCLUDED.stk_divi_rate,
  divi_pay_dt = EXCLUDED.divi_pay_dt,
  stk_div_pay_dt = EXCLUDED.stk_div_pay_dt,
  odd_pay_dt = EXCLUDED.odd_pay_dt,
  stk_kind = EXCLUDED.stk_kind,
  high_divi_gb = EXCLUDED.high_divi_gb,
  updated_at = CURRENT_TIMESTAMP;