-- KIS(한국투자증권) API의 "[국내주식] 시세 > 국내주식기간별시세(일/주/월/년)"의 데이터를 수집
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_daily_itemchartprice(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  stck_bsop_date TEXT NOT NULL,
  prdy_vrss TEXT,
  prdy_vrss_sign TEXT,
  prdy_ctrt TEXT,
  stck_prdy_clpr TEXT,
  acml_vol TEXT,
  acml_tr_pbmn TEXT,
  hts_kor_isnm TEXT,
  stck_prpr TEXT,
  stck_shrn_iscd TEXT,
  prdy_vol TEXT,
  stck_mxpr TEXT,
  stck_llam TEXT,
  stck_oprc TEXT,
  stck_hgpr TEXT,
  stck_lwpr TEXT,
  stck_prdy_oprc TEXT,
  stck_prdy_hgpr TEXT,
  stck_prdy_lwpr TEXT,
  askp TEXT,
  bidp TEXT,
  prdy_vrss_vol TEXT,
  vol_tnrt TEXT,
  stck_fcam TEXT,
  lstn_stcn TEXT,
  cpfn TEXT,
  hts_avls TEXT,
  per TEXT,
  eps TEXT,
  pbr TEXT,
  itewhol_loan_rmnd_ratem TEXT,
  stck_clpr TEXT,
  flng_cls_code TEXT,
  prtt_rate TEXT,
  mod_yn TEXT,
  revl_issu_reas TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- ticker와 stck_bsop_date를 조합하여 고유성을 보장
  UNIQUE (ticker, stck_bsop_date)
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_daily_itemchartprice IS '국내 주식 일별 시세 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_bsop_date IS '주식 영업 일자';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.prdy_vrss IS '전일 대비';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.prdy_vrss_sign IS '전일 대비 부호';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.prdy_ctrt IS '전일 대비율';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_prdy_clpr IS '주식 전일 종가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.acml_vol IS '누적 거래량';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.acml_tr_pbmn IS '누적 거래 대금';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.hts_kor_isnm IS 'HTS 한글 종목명';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_prpr IS '주식 현재가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_shrn_iscd IS '주식 단축 종목코드';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.prdy_vol IS '전일 거래량';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_mxpr IS '주식 상한가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_llam IS '주식 하한가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_oprc IS '주식 시가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_hgpr IS '주식 최고가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_lwpr IS '주식 최저가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_prdy_oprc IS '주식 전일 시가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_prdy_hgpr IS '주식 전일 최고가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_prdy_lwpr IS '주식 전일 최저가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.askp IS '매도호가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.bidp IS '매수호가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.prdy_vrss_vol IS '전일 대비 거래량';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.vol_tnrt IS '거래량 회전율';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_fcam IS '주식 액면가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.lstn_stcn IS '상장 주수';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.cpfn IS '자본금';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.hts_avls IS 'HTS 시가총액';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.per IS 'PER';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.eps IS 'EPS';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.pbr IS 'PBR';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.itewhol_loan_rmnd_ratem IS '전체 융자 잔고 비율';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.stck_clpr IS '주식 종가';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.flng_cls_code IS '락 구분 코드';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.prtt_rate IS '분할 비율';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.mod_yn IS '변경 여부';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.revl_issu_reas IS '재평가사유코드';
COMMENT ON COLUMN kr_stock_daily_itemchartprice.updated_at IS '데이터 마지막 수집 시간';