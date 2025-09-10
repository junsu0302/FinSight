-- KIS(한국투자증권) API의 "[국내주식] 시세 > 주식현재가 투자자"의 데이터를 수집
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_investor(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  stck_bsop_date TEXT NOT NULL,
  stck_clpr TEXT,
  prdy_vrss TEXT,
  prdy_vrss_sign TEXT,
  prsn_ntby_qty TEXT,
  frgn_ntby_qty TEXT,
  orgn_ntby_qty TEXT,
  prsn_ntby_tr_pbmn TEXT,
  frgn_ntby_tr_pbmn TEXT,
  orgn_ntby_tr_pbmn TEXT,
  prsn_shnu_vol TEXT,
  frgn_shnu_vol TEXT,
  orgn_shnu_vol TEXT,
  prsn_shnu_tr_pbmn TEXT,
  frgn_shnu_tr_pbmn TEXT,
  orgn_shnu_tr_pbmn TEXT,
  prsn_seln_vol TEXT,
  frgn_seln_vol TEXT,
  orgn_seln_vol TEXT,
  prsn_seln_tr_pbmn TEXT,
  frgn_seln_tr_pbmn TEXT,
  orgn_seln_tr_pbmn TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- ticker와 stck_bsop_date를 조합하여 고유성을 보장
  UNIQUE (ticker, stck_bsop_date)
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_investor IS '국내 주식 기간별 시세(투자자) 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_investor.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_investor.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_investor.stck_bsop_date IS '주식 영업 일자';
COMMENT ON COLUMN kr_stock_investor.stck_clpr IS '주식 종가';
COMMENT ON COLUMN kr_stock_investor.prdy_vrss IS '전일 대비';
COMMENT ON COLUMN kr_stock_investor.prdy_vrss_sign IS '전일 대비 부호';
COMMENT ON COLUMN kr_stock_investor.prsn_ntby_qty IS '개인 순매수 수량';
COMMENT ON COLUMN kr_stock_investor.frgn_ntby_qty IS '외국인 순매수 수량';
COMMENT ON COLUMN kr_stock_investor.orgn_ntby_qty IS '기관계 순매수 수량';
COMMENT ON COLUMN kr_stock_investor.prsn_ntby_tr_pbmn IS '개인 순매수 거래 대금';
COMMENT ON COLUMN kr_stock_investor.frgn_ntby_tr_pbmn IS '외국인 순매수 거래 대금';
COMMENT ON COLUMN kr_stock_investor.orgn_ntby_tr_pbmn IS '기관계 순매수 거래 대금';
COMMENT ON COLUMN kr_stock_investor.prsn_shnu_vol IS '개인 매수 거래량';
COMMENT ON COLUMN kr_stock_investor.frgn_shnu_vol IS '외국인 매수 거래량';
COMMENT ON COLUMN kr_stock_investor.orgn_shnu_vol IS '기관계 매수 거래량';
COMMENT ON COLUMN kr_stock_investor.prsn_shnu_tr_pbmn IS '개인 매수 거래 대금';
COMMENT ON COLUMN kr_stock_investor.frgn_shnu_tr_pbmn IS '외국인 매수 거래 대금';
COMMENT ON COLUMN kr_stock_investor.orgn_shnu_tr_pbmn IS '기관계 매수 거래 대금';
COMMENT ON COLUMN kr_stock_investor.prsn_seln_vol IS '개인 매도 거래량';
COMMENT ON COLUMN kr_stock_investor.frgn_seln_vol IS '외국인 매도 거래량';
COMMENT ON COLUMN kr_stock_investor.orgn_seln_vol IS '기관계 매도 거래량';
COMMENT ON COLUMN kr_stock_investor.prsn_seln_tr_pbmn IS '개인 매도 거래 대금';
COMMENT ON COLUMN kr_stock_investor.frgn_seln_tr_pbmn IS '외국인 매도 거래 대금';
COMMENT ON COLUMN kr_stock_investor.orgn_seln_tr_pbmn IS '기관계 매도 거래 대금';
COMMENT ON COLUMN kr_stock_investor.updated_at IS '데이터 마지막 수집 시간';