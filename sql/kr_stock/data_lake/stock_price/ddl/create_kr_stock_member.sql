-- KIS(한국투자증권) API의 "[국내주식] 시세 > 주식현재가 회원사"의 데이터를 수집
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_member(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL UNIQUE,
  seln_mbcr_no1 TEXT,
  seln_mbcr_no2 TEXT,
  seln_mbcr_no3 TEXT,
  seln_mbcr_no4 TEXT,
  seln_mbcr_no5 TEXT,
  seln_mbcr_name1 TEXT,
  seln_mbcr_name2 TEXT,
  seln_mbcr_name3 TEXT,
  seln_mbcr_name4 TEXT,
  seln_mbcr_name5 TEXT,
  total_seln_qty1 TEXT,
  total_seln_qty2 TEXT,
  total_seln_qty3 TEXT,
  total_seln_qty4 TEXT,
  total_seln_qty5 TEXT,
  seln_mbcr_rlim1 TEXT,
  seln_mbcr_rlim2 TEXT,
  seln_mbcr_rlim3 TEXT,
  seln_mbcr_rlim4 TEXT,
  seln_mbcr_rlim5 TEXT,
  seln_qty_icdc1 TEXT,
  seln_qty_icdc2 TEXT,
  seln_qty_icdc3 TEXT,
  seln_qty_icdc4 TEXT,
  seln_qty_icdc5 TEXT,
  shnu_mbcr_no1 TEXT,
  shnu_mbcr_no2 TEXT,
  shnu_mbcr_no3 TEXT,
  shnu_mbcr_no4 TEXT,
  shnu_mbcr_no5 TEXT,
  shnu_mbcr_name1 TEXT,
  shnu_mbcr_name2 TEXT,
  shnu_mbcr_name3 TEXT,
  shnu_mbcr_name4 TEXT,
  shnu_mbcr_name5 TEXT,
  total_shnu_qty1 TEXT,
  total_shnu_qty2 TEXT,
  total_shnu_qty3 TEXT,
  total_shnu_qty4 TEXT,
  total_shnu_qty5 TEXT,
  shnu_mbcr_rlim1 TEXT,
  shnu_mbcr_rlim2 TEXT,
  shnu_mbcr_rlim3 TEXT,
  shnu_mbcr_rlim4 TEXT,
  shnu_mbcr_rlim5 TEXT,
  shnu_qty_icdc1 TEXT,
  shnu_qty_icdc2 TEXT,
  shnu_qty_icdc3 TEXT,
  shnu_qty_icdc4 TEXT,
  shnu_qty_icdc5 TEXT,
  glob_total_seln_qty TEXT,
  glob_seln_rlim TEXT,
  glob_ntby_qty TEXT,
  glob_total_shnu_qty TEXT,
  glob_shnu_rlim TEXT,
  seln_mbcr_glob_yn_1 TEXT,
  seln_mbcr_glob_yn_2 TEXT,
  seln_mbcr_glob_yn_3 TEXT,
  seln_mbcr_glob_yn_4 TEXT,
  seln_mbcr_glob_yn_5 TEXT,
  shnu_mbcr_glob_yn_1 TEXT,
  shnu_mbcr_glob_yn_2 TEXT,
  shnu_mbcr_glob_yn_3 TEXT,
  shnu_mbcr_glob_yn_4 TEXT,
  shnu_mbcr_glob_yn_5 TEXT,
  glob_total_seln_qty_icdc TEXT,
  glob_total_shnu_qty_icdc TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_member IS '국내 주식 현재가 회원사 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_member.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_member.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_no1 IS '매도 회원사 번호1';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_no2 IS '매도 회원사 번호2';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_no3 IS '매도 회원사 번호3';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_no4 IS '매도 회원사 번호4';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_no5 IS '매도 회원사 번호5';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_name1 IS '매도 회원사 명1';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_name2 IS '매도 회원사 명2';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_name3 IS '매도 회원사 명3';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_name4 IS '매도 회원사 명4';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_name5 IS '매도 회원사 명5';
COMMENT ON COLUMN kr_stock_member.total_seln_qty1 IS '총 매도 수량1';
COMMENT ON COLUMN kr_stock_member.total_seln_qty2 IS '총 매도 수량2';
COMMENT ON COLUMN kr_stock_member.total_seln_qty3 IS '총 매도 수량3';
COMMENT ON COLUMN kr_stock_member.total_seln_qty4 IS '총 매도 수량4';
COMMENT ON COLUMN kr_stock_member.total_seln_qty5 IS '총 매도 수량5';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_rlim1 IS '매도 회원사 비중1';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_rlim2 IS '매도 회원사 비중2';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_rlim3 IS '매도 회원사 비중3';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_rlim4 IS '매도 회원사 비중4';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_rlim5 IS '매도 회원사 비중5';
COMMENT ON COLUMN kr_stock_member.seln_qty_icdc1 IS '매도 수량 증감1';
COMMENT ON COLUMN kr_stock_member.seln_qty_icdc2 IS '매도 수량 증감2';
COMMENT ON COLUMN kr_stock_member.seln_qty_icdc3 IS '매도 수량 증감3';
COMMENT ON COLUMN kr_stock_member.seln_qty_icdc4 IS '매도 수량 증감4';
COMMENT ON COLUMN kr_stock_member.seln_qty_icdc5 IS '매도 수량 증감5';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_no1 IS '매수 회원사 번호1';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_no2 IS '매수 회원사 번호2';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_no3 IS '매수 회원사 번호3';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_no4 IS '매수 회원사 번호4';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_no5 IS '매수 회원사 번호5';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_name1 IS '매수 회원사 명1';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_name2 IS '매수 회원사 명2';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_name3 IS '매수 회원사 명3';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_name4 IS '매수 회원사 명4';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_name5 IS '매수 회원사 명5';
COMMENT ON COLUMN kr_stock_member.total_shnu_qty1 IS '총 매수 수량1';
COMMENT ON COLUMN kr_stock_member.total_shnu_qty2 IS '총 매수 수량2';
COMMENT ON COLUMN kr_stock_member.total_shnu_qty3 IS '총 매수 수량3';
COMMENT ON COLUMN kr_stock_member.total_shnu_qty4 IS '총 매수 수량4';
COMMENT ON COLUMN kr_stock_member.total_shnu_qty5 IS '총 매수 수량5';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_rlim1 IS '매수 회원사 비중1';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_rlim2 IS '매수 회원사 비중2';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_rlim3 IS '매수 회원사 비중3';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_rlim4 IS '매수 회원사 비중4';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_rlim5 IS '매수 회원사 비중5';
COMMENT ON COLUMN kr_stock_member.shnu_qty_icdc1 IS '매수 수량 증감1';
COMMENT ON COLUMN kr_stock_member.shnu_qty_icdc2 IS '매수 수량 증감2';
COMMENT ON COLUMN kr_stock_member.shnu_qty_icdc3 IS '매수 수량 증감3';
COMMENT ON COLUMN kr_stock_member.shnu_qty_icdc4 IS '매수 수량 증감4';
COMMENT ON COLUMN kr_stock_member.shnu_qty_icdc5 IS '매수 수량 증감5';
COMMENT ON COLUMN kr_stock_member.glob_total_seln_qty IS '외국계 총 매도 수량';
COMMENT ON COLUMN kr_stock_member.glob_seln_rlim IS '외국계 매도 비중';
COMMENT ON COLUMN kr_stock_member.glob_ntby_qty IS '외국계 순매수 수량';
COMMENT ON COLUMN kr_stock_member.glob_total_shnu_qty IS '외국계 총 매수 수량';
COMMENT ON COLUMN kr_stock_member.glob_shnu_rlim IS '외국계 매수 비중';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_glob_yn_1 IS '매도 회원사 외국계 여부1';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_glob_yn_2 IS '매도 회원사 외국계 여부2';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_glob_yn_3 IS '매도 회원사 외국계 여부3';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_glob_yn_4 IS '매도 회원사 외국계 여부4';
COMMENT ON COLUMN kr_stock_member.seln_mbcr_glob_yn_5 IS '매도 회원사 외국계 여부5';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_glob_yn_1 IS '매수 회원사 외국계 여부1';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_glob_yn_2 IS '매수 회원사 외국계 여부2';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_glob_yn_3 IS '매수 회원사 외국계 여부3';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_glob_yn_4 IS '매수 회원사 외국계 여부4';
COMMENT ON COLUMN kr_stock_member.shnu_mbcr_glob_yn_5 IS '매수 회원사 외국계 여부5';
COMMENT ON COLUMN kr_stock_member.glob_total_seln_qty_icdc IS '외국계 총 매도 수량 증감';
COMMENT ON COLUMN kr_stock_member.glob_total_shnu_qty_icdc IS '외국계 총 매수 수량 증감';
COMMENT ON COLUMN kr_stock_member.updated_at IS '데이터 마지막 수집 시간';