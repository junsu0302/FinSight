-- KIS API의 '[국내주식] 종목정보 > 국내주식 종목추정실적'의 변환된 데이터를 저장하는 테이블
-- 이 테이블은 Data Mart 역할을 수행하며, 종목과 실적 기준 기간을 기준으로 데이터를 관리

CREATE TABLE IF NOT EXISTS kr_stock_estimate_perform (
  -- 복합 기본 키 (Composite Primary Key): 동일 종목이 여러 기간에 대한 추정 실적을 가질 수 있음
  ticker TEXT NOT NULL,          -- 종목코드
  period TEXT NOT NULL,          -- 실적 기준 기간 (예: 2022.12E)

  -- 기본 정보
  analyst TEXT,
  opinion TEXT,

  -- 성장성 지표
  revenue NUMERIC,
  revenue_yoy NUMERIC,
  operating_profit NUMERIC,
  operating_profit_yoy NUMERIC,
  net_income NUMERIC,
  net_income_yoy NUMERIC,
  
  -- 주당 가치 지표
  eps NUMERIC,
  eps_yoy NUMERIC,
  bps NUMERIC,

  -- 가치평가(Valuation) 지표
  per NUMERIC,
  pbr NUMERIC,
  psr NUMERIC,
  
  -- 수익성 및 효율성 지표
  roe NUMERIC,
  ebitda NUMERIC,
  ev_ebitda NUMERIC,
  
  -- 안정성 지표
  debt_ratio NUMERIC,
  interest_coverage_ratio NUMERIC,

  -- 데이터 수집 메타데이터
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- 기본 키 설정
  PRIMARY KEY (ticker, period)
);

-- 테이블 및 각 컬럼에 대한 설명(주석) 추가
COMMENT ON TABLE kr_stock_estimate_perform IS '국내 주식 종목추정실적 데이터 마트 테이블';
COMMENT ON COLUMN kr_stock_estimate_perform.ticker IS '종목코드';
COMMENT ON COLUMN kr_stock_estimate_perform.period IS '실적 기준 기간 (예: 2022.12E)';
COMMENT ON COLUMN kr_stock_estimate_perform.analyst IS '담당 애널리스트';
COMMENT ON COLUMN kr_stock_estimate_perform.opinion IS '투자의견';
COMMENT ON COLUMN kr_stock_estimate_perform.revenue IS '매출액';
COMMENT ON COLUMN kr_stock_estimate_perform.revenue_yoy IS '매출액 증감률 (YoY)';
COMMENT ON COLUMN kr_stock_estimate_perform.operating_profit IS '영업이익';
COMMENT ON COLUMN kr_stock_estimate_perform.operating_profit_yoy IS '영업이익 증감률 (YoY)';
COMMENT ON COLUMN kr_stock_estimate_perform.net_income IS '당기순이익';
COMMENT ON COLUMN kr_stock_estimate_perform.net_income_yoy IS '당기순이익 증감률 (YoY)';
COMMENT ON COLUMN kr_stock_estimate_perform.eps IS 'EPS (주당순이익)';
COMMENT ON COLUMN kr_stock_estimate_perform.eps_yoy IS 'EPS 증감률 (YoY)';
COMMENT ON COLUMN kr_stock_estimate_perform.bps IS 'BPS (주당순자산가치)';
COMMENT ON COLUMN kr_stock_estimate_perform.per IS 'PER (주가수익비율)';
COMMENT ON COLUMN kr_stock_estimate_perform.pbr IS 'PBR (주가순자산비율)';
COMMENT ON COLUMN kr_stock_estimate_perform.psr IS 'PSR (주가매출비율)';
COMMENT ON COLUMN kr_stock_estimate_perform.roe IS 'ROE (자기자본이익률)';
COMMENT ON COLUMN kr_stock_estimate_perform.ebitda IS 'EBITDA';
COMMENT ON COLUMN kr_stock_estimate_perform.ev_ebitda IS 'EV/EBITDA';
COMMENT ON COLUMN kr_stock_estimate_perform.debt_ratio IS '부채비율';
COMMENT ON COLUMN kr_stock_estimate_perform.interest_coverage_ratio IS '이자보상배율';
COMMENT ON COLUMN kr_stock_estimate_perform.updated_at IS '데이터 마지막 수집 시간';