-- kr_stock_estimate_perform 테이블에 데이터를 삽입하거나, 
-- (ticker, period)가 동일한 데이터가 이미 존재하는 경우 최신 정보로 업데이트합니다. (UPSERT)
INSERT INTO kr_stock_estimate_perform (
  ticker, period, analyst, opinion, revenue, revenue_yoy, 
  operating_profit, operating_profit_yoy, net_income, net_income_yoy, 
  eps, eps_yoy, bps, per, pbr, psr, roe, ebitda, ev_ebitda, 
  debt_ratio, interest_coverage_ratio
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
ON CONFLICT (ticker, period) DO UPDATE SET
  analyst = EXCLUDED.analyst,
  opinion = EXCLUDED.opinion,
  revenue = EXCLUDED.revenue,
  revenue_yoy = EXCLUDED.revenue_yoy,
  operating_profit = EXCLUDED.operating_profit,
  operating_profit_yoy = EXCLUDED.operating_profit_yoy,
  net_income = EXCLUDED.net_income,
  net_income_yoy = EXCLUDED.net_income_yoy,
  eps = EXCLUDED.eps,
  eps_yoy = EXCLUDED.eps_yoy,
  bps = EXCLUDED.bps,
  per = EXCLUDED.per,
  pbr = EXCLUDED.pbr,
  psr = EXCLUDED.psr,
  roe = EXCLUDED.roe,
  ebitda = EXCLUDED.ebitda,
  ev_ebitda = EXCLUDED.ev_ebitda,
  debt_ratio = EXCLUDED.debt_ratio,
  interest_coverage_ratio = EXCLUDED.interest_coverage_ratio,
  updated_at = CURRENT_TIMESTAMP;