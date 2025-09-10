-- KIS API의 '[국내주식] 종목정보 > 국내주식 증권사별 투자의견' 데이터를 저장하는 테이블
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_invest_opbysec (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  stck_bsop_date TEXT NOT NULL,          -- 주식영업일자
  stck_shrn_iscd TEXT NOT NULL,          -- 주식단축종목코드
  mbcr_name TEXT NOT NULL,               -- 회원사명

  -- API로부터 수집되는 상세 데이터
  hts_kor_isnm TEXT,                     -- HTS한글종목명
  invt_opnn TEXT,                        -- 투자의견
  invt_opnn_cls_code TEXT,               -- 투자의견구분코드
  rgbf_invt_opnn TEXT,                   -- 직전투자의견
  rgbf_invt_opnn_cls_code TEXT,          -- 직전투자의견구분코드
  stck_prpr TEXT,                        -- 주식현재가
  prdy_vrss TEXT,                        -- 전일대비
  prdy_vrss_sign TEXT,                   -- 전일대비부호
  prdy_ctrt TEXT,                        -- 전일대비율
  hts_goal_prc TEXT,                     -- HTS목표가격
  stck_prdy_clpr TEXT,                   -- 주식전일종가
  stft_esdg TEXT,                        -- 주식선물괴리도
  dprt TEXT,                             -- 괴리율

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- (종목코드, 영업일자, 회원사명)을 조합하여 고유성을 보장
  UNIQUE (stck_shrn_iscd, stck_bsop_date, mbcr_name)
);

-- 테이블 및 각 컬럼에 대한 설명(주석) 추가
COMMENT ON TABLE kr_stock_invest_opbysec IS '국내 주식 증권사별 투자의견 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_invest_opbysec.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_invest_opbysec.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_invest_opbysec.stck_bsop_date IS '주식영업일자';
COMMENT ON COLUMN kr_stock_invest_opbysec.stck_shrn_iscd IS '주식단축종목코드';
COMMENT ON COLUMN kr_stock_invest_opbysec.mbcr_name IS '회원사명';
COMMENT ON COLUMN kr_stock_invest_opbysec.hts_kor_isnm IS 'HTS한글종목명';
COMMENT ON COLUMN kr_stock_invest_opbysec.invt_opnn IS '투자의견';
COMMENT ON COLUMN kr_stock_invest_opbysec.invt_opnn_cls_code IS '투자의견구분코드';
COMMENT ON COLUMN kr_stock_invest_opbysec.rgbf_invt_opnn IS '직전투자의견';
COMMENT ON COLUMN kr_stock_invest_opbysec.rgbf_invt_opnn_cls_code IS '직전투자의견구분코드';
COMMENT ON COLUMN kr_stock_invest_opbysec.stck_prpr IS '주식현재가';
COMMENT ON COLUMN kr_stock_invest_opbysec.prdy_vrss IS '전일대비';
COMMENT ON COLUMN kr_stock_invest_opbysec.prdy_vrss_sign IS '전일대비부호';
COMMENT ON COLUMN kr_stock_invest_opbysec.prdy_ctrt IS '전일대비율';
COMMENT ON COLUMN kr_stock_invest_opbysec.hts_goal_prc IS 'HTS목표가격';
COMMENT ON COLUMN kr_stock_invest_opbysec.stck_prdy_clpr IS '주식전일종가';
COMMENT ON COLUMN kr_stock_invest_opbysec.stft_esdg IS '주식선물괴리도';
COMMENT ON COLUMN kr_stock_invest_opbysec.dprt IS '괴리율';
COMMENT ON COLUMN kr_stock_invest_opbysec.updated_at IS '데이터 마지막 수집 시간';