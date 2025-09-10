-- KIS(한국투자증권) API의 "[국내주식] 시세 > 주식현재가 시세2"의 데이터를 수집
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_price_detail(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL UNIQUE,
  rprs_mrkt_kor_name TEXT,
  new_hgpr_lwpr_cls_code TEXT,
  mxpr_llam_cls_code TEXT,
  crdt_able_yn TEXT,
  stck_mxpr TEXT,
  elw_pblc_yn TEXT,
  prdy_clpr_vrss_oprc_rate TEXT,
  crdt_rate TEXT,
  marg_rate TEXT,
  lwpr_vrss_prpr TEXT,
  lwpr_vrss_prpr_sign TEXT,
  prdy_clpr_vrss_lwpr_rate TEXT,
  stck_lwpr TEXT,
  hgpr_vrss_prpr TEXT,
  hgpr_vrss_prpr_sign TEXT,
  prdy_clpr_vrss_hgpr_rate TEXT,
  stck_hgpr TEXT,
  oprc_vrss_prpr TEXT,
  oprc_vrss_prpr_sign TEXT,
  mang_issu_yn TEXT,
  divi_app_cls_code TEXT,
  short_over_yn TEXT,
  mrkt_warn_cls_code TEXT,
  invt_caful_yn TEXT,
  stange_runup_yn TEXT,
  ssts_hot_yn TEXT,
  low_current_yn TEXT,
  vi_cls_code TEXT,
  short_over_cls_code TEXT,
  stck_llam TEXT,
  new_lstn_cls_name TEXT,
  vlnt_deal_cls_name TEXT,
  flng_cls_name TEXT,
  revl_issu_reas_name TEXT,
  mrkt_warn_cls_name TEXT,
  stck_sdpr TEXT,
  bstp_cls_code TEXT,
  stck_prdy_clpr TEXT,
  insn_pbnt_yn TEXT,
  fcam_mod_cls_name TEXT,
  stck_prpr TEXT,
  prdy_vrss TEXT,
  prdy_vrss_sign TEXT,
  prdy_ctrt TEXT,
  acml_tr_pbmn TEXT,
  acml_vol TEXT,
  prdy_vrss_vol_rate TEXT,
  bstp_kor_isnm TEXT,
  sltr_yn TEXT,
  trht_yn TEXT,
  oprc_rang_cont_yn TEXT,
  vlnt_fin_cls_code TEXT,
  stck_oprc TEXT,
  prdy_vol TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_price_detail IS '국내 주식 현재가 상세 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_price_detail.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_price_detail.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_price_detail.rprs_mrkt_kor_name IS '대표 시장 한글 명';
COMMENT ON COLUMN kr_stock_price_detail.new_hgpr_lwpr_cls_code IS '신 고가 저가 구분 코드';
COMMENT ON COLUMN kr_stock_price_detail.mxpr_llam_cls_code IS '상하한가 구분 코드';
COMMENT ON COLUMN kr_stock_price_detail.crdt_able_yn IS '신용 가능 여부';
COMMENT ON COLUMN kr_stock_price_detail.stck_mxpr IS '주식 상한가';
COMMENT ON COLUMN kr_stock_price_detail.elw_pblc_yn IS 'ELW 발행 여부';
COMMENT ON COLUMN kr_stock_price_detail.prdy_clpr_vrss_oprc_rate IS '전일 종가 대비 시가2 비율';
COMMENT ON COLUMN kr_stock_price_detail.crdt_rate IS '신용 비율';
COMMENT ON COLUMN kr_stock_price_detail.marg_rate IS '증거금 비율';
COMMENT ON COLUMN kr_stock_price_detail.lwpr_vrss_prpr IS '최저가 대비 현재가';
COMMENT ON COLUMN kr_stock_price_detail.lwpr_vrss_prpr_sign IS '최저가 대비 현재가 부호';
COMMENT ON COLUMN kr_stock_price_detail.prdy_clpr_vrss_lwpr_rate IS '전일 종가 대비 최저가 비율';
COMMENT ON COLUMN kr_stock_price_detail.stck_lwpr IS '주식 최저가';
COMMENT ON COLUMN kr_stock_price_detail.hgpr_vrss_prpr IS '최고가 대비 현재가';
COMMENT ON COLUMN kr_stock_price_detail.hgpr_vrss_prpr_sign IS '최고가 대비 현재가 부호';
COMMENT ON COLUMN kr_stock_price_detail.prdy_clpr_vrss_hgpr_rate IS '전일 종가 대비 최고가 비율';
COMMENT ON COLUMN kr_stock_price_detail.stck_hgpr IS '주식 최고가';
COMMENT ON COLUMN kr_stock_price_detail.oprc_vrss_prpr IS '시가2 대비 현재가';
COMMENT ON COLUMN kr_stock_price_detail.oprc_vrss_prpr_sign IS '시가2 대비 현재가 부호';
COMMENT ON COLUMN kr_stock_price_detail.mang_issu_yn IS '관리 종목 여부';
COMMENT ON COLUMN kr_stock_price_detail.divi_app_cls_code IS '동시호가배분처리코드';
COMMENT ON COLUMN kr_stock_price_detail.short_over_yn IS '단기과열여부';
COMMENT ON COLUMN kr_stock_price_detail.mrkt_warn_cls_code IS '시장경고코드';
COMMENT ON COLUMN kr_stock_price_detail.invt_caful_yn IS '투자유의여부';
COMMENT ON COLUMN kr_stock_price_detail.stange_runup_yn IS '이상급등여부';
COMMENT ON COLUMN kr_stock_price_detail.ssts_hot_yn IS '공매도과열 여부';
COMMENT ON COLUMN kr_stock_price_detail.low_current_yn IS '저유동성 종목 여부';
COMMENT ON COLUMN kr_stock_price_detail.vi_cls_code IS 'VI적용구분코드';
COMMENT ON COLUMN kr_stock_price_detail.short_over_cls_code IS '단기과열구분코드';
COMMENT ON COLUMN kr_stock_price_detail.stck_llam IS '주식 하한가';
COMMENT ON COLUMN kr_stock_price_detail.new_lstn_cls_name IS '신규 상장 구분 명';
COMMENT ON COLUMN kr_stock_price_detail.vlnt_deal_cls_name IS '임의 매매 구분 명';
COMMENT ON COLUMN kr_stock_price_detail.flng_cls_name IS '락 구분 이름';
COMMENT ON COLUMN kr_stock_price_detail.revl_issu_reas_name IS '재평가 종목 사유 명';
COMMENT ON COLUMN kr_stock_price_detail.mrkt_warn_cls_name IS '시장 경고 구분 명';
COMMENT ON COLUMN kr_stock_price_detail.stck_sdpr IS '주식 기준가';
COMMENT ON COLUMN kr_stock_price_detail.bstp_cls_code IS '업종 구분 코드';
COMMENT ON COLUMN kr_stock_price_detail.stck_prdy_clpr IS '주식 전일 종가';
COMMENT ON COLUMN kr_stock_price_detail.insn_pbnt_yn IS '불성실 공시 여부';
COMMENT ON COLUMN kr_stock_price_detail.fcam_mod_cls_name IS '액면가 변경 구분 명';
COMMENT ON COLUMN kr_stock_price_detail.stck_prpr IS '주식 현재가';
COMMENT ON COLUMN kr_stock_price_detail.prdy_vrss IS '전일 대비';
COMMENT ON COLUMN kr_stock_price_detail.prdy_vrss_sign IS '전일 대비 부호';
COMMENT ON COLUMN kr_stock_price_detail.prdy_ctrt IS '전일 대비율';
COMMENT ON COLUMN kr_stock_price_detail.acml_tr_pbmn IS '누적 거래 대금';
COMMENT ON COLUMN kr_stock_price_detail.acml_vol IS '누적 거래량';
COMMENT ON COLUMN kr_stock_price_detail.prdy_vrss_vol_rate IS '전일 대비 거래량 비율';
COMMENT ON COLUMN kr_stock_price_detail.bstp_kor_isnm IS '업종 한글 종목명';
COMMENT ON COLUMN kr_stock_price_detail.sltr_yn IS '정리매매 여부';
COMMENT ON COLUMN kr_stock_price_detail.trht_yn IS '거래정지 여부';
COMMENT ON COLUMN kr_stock_price_detail.oprc_rang_cont_yn IS '시가 범위 연장 여부';
COMMENT ON COLUMN kr_stock_price_detail.vlnt_fin_cls_code IS '임의 종료 구분 코드';
COMMENT ON COLUMN kr_stock_price_detail.stck_oprc IS '주식 시가2';
COMMENT ON COLUMN kr_stock_price_detail.prdy_vol IS '전일 거래량';
COMMENT ON COLUMN kr_stock_price_detail.updated_at IS '데이터 마지막 수집 시간';