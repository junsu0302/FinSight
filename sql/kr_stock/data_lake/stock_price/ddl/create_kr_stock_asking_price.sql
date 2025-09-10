-- KIS(한국투자증권) API의 "[국내주식] 시세 > 국내주식 현재가 호가/예상체결"의 데이터를 수집
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_asking_price(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL UNIQUE,
  aspr_acpt_hour TEXT,
  askp1 TEXT,
  askp2 TEXT,
  askp3 TEXT,
  askp4 TEXT,
  askp5 TEXT,
  askp6 TEXT,
  askp7 TEXT,
  askp8 TEXT,
  askp9 TEXT,
  askp10 TEXT,
  bidp1 TEXT,
  bidp2 TEXT,
  bidp3 TEXT,
  bidp4 TEXT,
  bidp5 TEXT,
  bidp6 TEXT,
  bidp7 TEXT,
  bidp8 TEXT,
  bidp9 TEXT,
  bidp10 TEXT,
  askp_rsqn1 TEXT,
  askp_rsqn2 TEXT,
  askp_rsqn3 TEXT,
  askp_rsqn4 TEXT,
  askp_rsqn5 TEXT,
  askp_rsqn6 TEXT,
  askp_rsqn7 TEXT,
  askp_rsqn8 TEXT,
  askp_rsqn9 TEXT,
  askp_rsqn10 TEXT,
  bidp_rsqn1 TEXT,
  bidp_rsqn2 TEXT,
  bidp_rsqn3 TEXT,
  bidp_rsqn4 TEXT,
  bidp_rsqn5 TEXT,
  bidp_rsqn6 TEXT,
  bidp_rsqn7 TEXT,
  bidp_rsqn8 TEXT,
  bidp_rsqn9 TEXT,
  bidp_rsqn10 TEXT,
  askp_rsqn_icdc1 TEXT,
  askp_rsqn_icdc2 TEXT,
  askp_rsqn_icdc3 TEXT,
  askp_rsqn_icdc4 TEXT,
  askp_rsqn_icdc5 TEXT,
  askp_rsqn_icdc6 TEXT,
  askp_rsqn_icdc7 TEXT,
  askp_rsqn_icdc8 TEXT,
  askp_rsqn_icdc9 TEXT,
  askp_rsqn_icdc10 TEXT,
  bidp_rsqn_icdc1 TEXT,
  bidp_rsqn_icdc2 TEXT,
  bidp_rsqn_icdc3 TEXT,
  bidp_rsqn_icdc4 TEXT,
  bidp_rsqn_icdc5 TEXT,
  bidp_rsqn_icdc6 TEXT,
  bidp_rsqn_icdc7 TEXT,
  bidp_rsqn_icdc8 TEXT,
  bidp_rsqn_icdc9 TEXT,
  bidp_rsqn_icdc10 TEXT,
  total_askp_rsqn TEXT,
  total_bidp_rsqn TEXT,
  total_askp_rsqn_icdc TEXT,
  total_bidp_rsqn_icdc TEXT,
  ovtm_total_askp_icdc TEXT,
  ovtm_total_bidp_icdc TEXT,
  ovtm_total_askp_rsqn TEXT,
  ovtm_total_bidp_rsqn TEXT,
  ntby_aspr_rsqn TEXT,
  new_mkop_cls_code TEXT,
  antc_mkop_cls_code TEXT,
  stck_prpr TEXT,
  stck_oprc TEXT,
  stck_hgpr TEXT,
  stck_lwpr TEXT,
  stck_sdpr TEXT,
  antc_cnpr TEXT,
  antc_cntg_vrss_sign TEXT,
  antc_cntg_vrss TEXT,
  antc_cntg_prdy_ctrt TEXT,
  antc_vol TEXT,
  stck_shrn_iscd TEXT,
  vi_cls_code TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_asking_price IS '국내 주식 현재가 호가 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_asking_price.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_asking_price.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_asking_price.aspr_acpt_hour IS '호가 접수 시간';
COMMENT ON COLUMN kr_stock_asking_price.askp1 IS '매도호가1';
COMMENT ON COLUMN kr_stock_asking_price.askp2 IS '매도호가2';
COMMENT ON COLUMN kr_stock_asking_price.askp3 IS '매도호가3';
COMMENT ON COLUMN kr_stock_asking_price.askp4 IS '매도호가4';
COMMENT ON COLUMN kr_stock_asking_price.askp5 IS '매도호가5';
COMMENT ON COLUMN kr_stock_asking_price.askp6 IS '매도호가6';
COMMENT ON COLUMN kr_stock_asking_price.askp7 IS '매도호가7';
COMMENT ON COLUMN kr_stock_asking_price.askp8 IS '매도호가8';
COMMENT ON COLUMN kr_stock_asking_price.askp9 IS '매도호가9';
COMMENT ON COLUMN kr_stock_asking_price.askp10 IS '매도호가10';
COMMENT ON COLUMN kr_stock_asking_price.bidp1 IS '매수호가1';
COMMENT ON COLUMN kr_stock_asking_price.bidp2 IS '매수호가2';
COMMENT ON COLUMN kr_stock_asking_price.bidp3 IS '매수호가3';
COMMENT ON COLUMN kr_stock_asking_price.bidp4 IS '매수호가4';
COMMENT ON COLUMN kr_stock_asking_price.bidp5 IS '매수호가5';
COMMENT ON COLUMN kr_stock_asking_price.bidp6 IS '매수호가6';
COMMENT ON COLUMN kr_stock_asking_price.bidp7 IS '매수호가7';
COMMENT ON COLUMN kr_stock_asking_price.bidp8 IS '매수호가8';
COMMENT ON COLUMN kr_stock_asking_price.bidp9 IS '매수호가9';
COMMENT ON COLUMN kr_stock_asking_price.bidp10 IS '매수호가10';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn1 IS '매도호가 잔량1';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn2 IS '매도호가 잔량2';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn3 IS '매도호가 잔량3';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn4 IS '매도호가 잔량4';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn5 IS '매도호가 잔량5';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn6 IS '매도호가 잔량6';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn7 IS '매도호가 잔량7';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn8 IS '매도호가 잔량8';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn9 IS '매도호가 잔량9';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn10 IS '매도호가 잔량10';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn1 IS '매수호가 잔량1';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn2 IS '매수호가 잔량2';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn3 IS '매수호가 잔량3';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn4 IS '매수호가 잔량4';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn5 IS '매수호가 잔량5';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn6 IS '매수호가 잔량6';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn7 IS '매수호가 잔량7';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn8 IS '매수호가 잔량8';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn9 IS '매수호가 잔량9';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn10 IS '매수호가 잔량10';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc1 IS '매도호가 잔량 증감1';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc2 IS '매도호가 잔량 증감2';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc3 IS '매도호가 잔량 증감3';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc4 IS '매도호가 잔량 증감4';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc5 IS '매도호가 잔량 증감5';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc6 IS '매도호가 잔량 증감6';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc7 IS '매도호가 잔량 증감7';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc8 IS '매도호가 잔량 증감8';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc9 IS '매도호가 잔량 증감9';
COMMENT ON COLUMN kr_stock_asking_price.askp_rsqn_icdc10 IS '매도호가 잔량 증감10';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc1 IS '매수호가 잔량 증감1';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc2 IS '매수호가 잔량 증감2';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc3 IS '매수호가 잔량 증감3';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc4 IS '매수호가 잔량 증감4';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc5 IS '매수호가 잔량 증감5';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc6 IS '매수호가 잔량 증감6';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc7 IS '매수호가 잔량 증감7';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc8 IS '매수호가 잔량 증감8';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc9 IS '매수호가 잔량 증감9';
COMMENT ON COLUMN kr_stock_asking_price.bidp_rsqn_icdc10 IS '매수호가 잔량 증감10';
COMMENT ON COLUMN kr_stock_asking_price.total_askp_rsqn IS '총 매도호가 잔량';
COMMENT ON COLUMN kr_stock_asking_price.total_bidp_rsqn IS '총 매수호가 잔량';
COMMENT ON COLUMN kr_stock_asking_price.total_askp_rsqn_icdc IS '총 매도호가 잔량 증감';
COMMENT ON COLUMN kr_stock_asking_price.total_bidp_rsqn_icdc IS '총 매수호가 잔량 증감';
COMMENT ON COLUMN kr_stock_asking_price.ovtm_total_askp_icdc IS '시간외 총 매도호가 증감';
COMMENT ON COLUMN kr_stock_asking_price.ovtm_total_bidp_icdc IS '시간외 총 매수호가 증감';
COMMENT ON COLUMN kr_stock_asking_price.ovtm_total_askp_rsqn IS '시간외 총 매도호가 잔량';
COMMENT ON COLUMN kr_stock_asking_price.ovtm_total_bidp_rsqn IS '시간외 총 매수호가 잔량';
COMMENT ON COLUMN kr_stock_asking_price.ntby_aspr_rsqn IS '순매수 호가 잔량';
COMMENT ON COLUMN kr_stock_asking_price.new_mkop_cls_code IS '신 장운영 구분 코드';
COMMENT ON COLUMN kr_stock_asking_price.antc_mkop_cls_code IS '예상 장운영 구분 코드';
COMMENT ON COLUMN kr_stock_asking_price.stck_prpr IS '주식 현재가';
COMMENT ON COLUMN kr_stock_asking_price.stck_oprc IS '주식 시가2';
COMMENT ON COLUMN kr_stock_asking_price.stck_hgpr IS '주식 최고가';
COMMENT ON COLUMN kr_stock_asking_price.stck_lwpr IS '주식 최저가';
COMMENT ON COLUMN kr_stock_asking_price.stck_sdpr IS '주식 기준가';
COMMENT ON COLUMN kr_stock_asking_price.antc_cnpr IS '예상 체결가';
COMMENT ON COLUMN kr_stock_asking_price.antc_cntg_vrss_sign IS '예상 체결 대비 부호';
COMMENT ON COLUMN kr_stock_asking_price.antc_cntg_vrss IS '예상 체결 대비';
COMMENT ON COLUMN kr_stock_asking_price.antc_cntg_prdy_ctrt IS '예상 체결 전일 대비율';
COMMENT ON COLUMN kr_stock_asking_price.antc_vol IS '예상 거래량';
COMMENT ON COLUMN kr_stock_asking_price.stck_shrn_iscd IS '주식 단축 종목코드';
COMMENT ON COLUMN kr_stock_asking_price.vi_cls_code IS 'VI적용구분코드';
COMMENT ON COLUMN kr_stock_asking_price.updated_at IS '데이터 마지막 수집 시간';