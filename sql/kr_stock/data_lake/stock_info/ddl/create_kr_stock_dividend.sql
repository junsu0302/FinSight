-- KIS API의 '[국내주식] 종목정보 > 예탁원정보(배당일정)' 데이터를 저장하는 테이블
-- 이 테이블은 Data Lake 역할을 수행하며, 종목과 배당기준일을 기준으로 데이터를 관리

CREATE TABLE IF NOT EXISTS kr_stock_dividend (
  ticker TEXT NOT NULL,
  record_date TEXT NOT NULL,
  sht_cd TEXT NOT NULL,
  isin_name TEXT,
  divi_kind TEXT NOT NULL,
  face_val TEXT,
  per_sto_divi_amt TEXT,
  divi_rate TEXT,
  stk_divi_rate TEXT,
  divi_pay_dt TEXT,
  stk_div_pay_dt TEXT,
  odd_pay_dt TEXT,
  stk_kind TEXT,
  high_divi_gb TEXT,

  -- 데이터 수집 메타데이터
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- 기본 키 설정
  PRIMARY KEY (ticker, record_date)
);

-- 테이블 및 각 컬럼에 대한 설명(주석) 추가
COMMENT ON TABLE kr_stock_dividend IS '국내 주식 배당일정 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_dividend.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_dividend.record_date IS '기준일';
COMMENT ON COLUMN kr_stock_dividend.sht_cd IS '종목코드';
COMMENT ON COLUMN kr_stock_dividend.isin_name IS '종목명';
COMMENT ON COLUMN kr_stock_dividend.divi_kind IS '배당종류';
COMMENT ON COLUMN kr_stock_dividend.face_val IS '액면가';
COMMENT ON COLUMN kr_stock_dividend.per_sto_divi_amt IS '주당 현금배당금';
COMMENT ON COLUMN kr_stock_dividend.divi_rate IS '현금배당률(%)';
COMMENT ON COLUMN kr_stock_dividend.stk_divi_rate IS '주식배당률(%)';
COMMENT ON COLUMN kr_stock_dividend.divi_pay_dt IS '현금배당금 지급일';
COMMENT ON COLUMN kr_stock_dividend.stk_div_pay_dt IS '주식배당 지급일';
COMMENT ON COLUMN kr_stock_dividend.odd_pay_dt IS '단주대금 지급일';
COMMENT ON COLUMN kr_stock_dividend.stk_kind IS '주식종류';
COMMENT ON COLUMN kr_stock_dividend.high_divi_gb IS '고배당종목여부';
COMMENT ON COLUMN kr_stock_dividend.updated_at IS '데이터 마지막 수집 시간';