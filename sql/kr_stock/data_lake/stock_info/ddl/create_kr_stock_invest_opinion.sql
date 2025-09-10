-- KIS API의 '[국내주식] 종목정보 > 국내주식 종목투자의견' 데이터를 저장하는 테이블
-- 이 테이블은 종목, 영업일자, 회원사명을 기준으로 데이터를 관리

CREATE TABLE IF NOT EXISTS kr_stock_invest_opinion (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,          -- 데이터 조회의 기준이 된 표준 종목코드 (6자리)
  stck_bsop_date TEXT NOT NULL,  -- 주식 영업일자
  mbcr_name TEXT NOT NULL,       -- 회원사명 (증권사)

  -- API로부터 수집되는 상세 데이터
  invt_opnn TEXT,
  invt_opnn_cls_code TEXT,
  rgbf_invt_opnn TEXT,
  rgbf_invt_opnn_cls_code TEXT,
  hts_goal_prc INTEGER,
  stck_prdy_clpr INTEGER,
  stck_nday_esdg NUMERIC,
  nday_dprt NUMERIC,
  stft_esdg NUMERIC,
  dprt NUMERIC,

  -- 데이터 수집 메타데이터
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- (종목코드, 영업일자, 회원사명)을 조합하여 고유성을 보장
  UNIQUE (ticker, stck_bsop_date, mbcr_name)
);

-- 테이블 및 각 컬럼에 대한 설명(주석) 추가
COMMENT ON TABLE kr_stock_invest_opinion IS '국내 주식 종목 투자의견 데이터 테이블';
COMMENT ON COLUMN kr_stock_invest_opinion.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_invest_opinion.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_invest_opinion.stck_bsop_date IS '주식 영업일자';
COMMENT ON COLUMN kr_stock_invest_opinion.mbcr_name IS '회원사명 (증권사)';
COMMENT ON COLUMN kr_stock_invest_opinion.invt_opnn IS '투자의견';
COMMENT ON COLUMN kr_stock_invest_opinion.invt_opnn_cls_code IS '투자의견 구분코드';
COMMENT ON COLUMN kr_stock_invest_opinion.rgbf_invt_opnn IS '직전 투자의견';
COMMENT ON COLUMN kr_stock_invest_opinion.rgbf_invt_opnn_cls_code IS '직전 투자의견 구분코드';
COMMENT ON COLUMN kr_stock_invest_opinion.hts_goal_prc IS 'HTS 목표가격';
COMMENT ON COLUMN kr_stock_invest_opinion.stck_prdy_clpr IS '주식 전일종가';
COMMENT ON COLUMN kr_stock_invest_opinion.stck_nday_esdg IS '주식 N일 괴리도';
COMMENT ON COLUMN kr_stock_invest_opinion.nday_dprt IS 'N일 괴리율';
COMMENT ON COLUMN kr_stock_invest_opinion.stft_esdg IS '주식선물 괴리도';
COMMENT ON COLUMN kr_stock_invest_opinion.dprt IS '괴리율';
COMMENT ON COLUMN kr_stock_invest_opinion.updated_at IS '데이터 마지막 수집 시간';