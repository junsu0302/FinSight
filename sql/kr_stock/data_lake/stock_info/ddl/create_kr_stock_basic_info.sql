-- KIS(한국투자증권) API의 "[국내주식] 종목정보 > 주식기본조회"의 데이터를 수집 
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

/*
[데이터베이스 설계 노트]
- 기본 키 (Primary Key):
  - id (일련번호, SERIAL): 시스템이 생성하는 인조 키.

- 후보 키 (Candidate Key):
  - ticker (종목코드, TEXT): 비즈니스적으로 유일성을 가지는 키.

- 'id'를 기본 키로 채택한 사유:
  1. 조인 성능: 고정 크기 숫자 타입인 'id'는 가변 크기 문자열인 'ticker'에 비해
     테이블 조인(JOIN) 시 월등한 성능을 제공한다. (참조: Index Size and Performance)
  2. 불변성: 'ticker'는 문자를 포함할 수 있고('00104K') 선행 '0'이 의미를 가지므로
     숫자 타입으로 변환할 수 없다. 또한 비즈니스 규칙 변경 가능성을 고려할 때,
     절대 변하지 않는 'id'를 사용하는 것이 유지보수에 유리하다.
*/

CREATE TABLE IF NOT EXISTS kr_stock_basic_info(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL UNIQUE,
  
  pdno TEXT,
  prdt_type_cd TEXT,
  mket_id_cd TEXT,
  scty_grp_id_cd TEXT,
  excg_dvsn_cd TEXT,
  setl_mmdd TEXT,
  lstg_stqt TEXT,
  lstg_cptl_amt TEXT,
  cpta TEXT,
  papr TEXT,
  issu_pric TEXT,
  kospi200_item_yn TEXT,
  scts_mket_lstg_dt TEXT,
  scts_mket_lstg_abol_dt TEXT,
  kosdaq_mket_lstg_dt TEXT,
  kosdaq_mket_lstg_abol_dt TEXT,
  frbd_mket_lstg_dt TEXT,
  frbd_mket_lstg_abol_dt TEXT,
  reits_kind_cd TEXT,
  etf_dvsn_cd TEXT,
  oilf_fund_yn TEXT,
  idx_bztp_lcls_cd TEXT,
  idx_bztp_mcls_cd TEXT,
  idx_bztp_scls_cd TEXT,
  stck_kind_cd TEXT,
  mfnd_opng_dt TEXT,
  mfnd_end_dt TEXT,
  dpsi_erlm_cncl_dt TEXT,
  etf_cu_qty TEXT,
  prdt_name TEXT,
  prdt_name120 TEXT,
  prdt_abrv_name TEXT,
  std_pdno TEXT,
  prdt_eng_name TEXT,
  prdt_eng_name120 TEXT,
  prdt_eng_abrv_name TEXT,
  dpsi_aptm_erlm_yn TEXT,
  etf_txtn_type_cd TEXT,
  etf_type_cd TEXT,
  lstg_abol_dt TEXT,
  nwst_odst_dvsn_cd TEXT,
  sbst_pric TEXT,
  thco_sbst_pric TEXT,
  thco_sbst_pric_chng_dt TEXT,
  tr_stop_yn TEXT,
  admn_item_yn TEXT,
  thdt_clpr TEXT,
  bfdy_clpr TEXT,
  clpr_chng_dt TEXT,
  std_idst_clsf_cd TEXT,
  std_idst_clsf_cd_name TEXT,
  idx_bztp_lcls_cd_name TEXT,
  idx_bztp_mcls_cd_name TEXT,
  idx_bztp_scls_cd_name TEXT,
  ocr_no TEXT,
  crfd_item_yn TEXT,
  elec_scty_yn TEXT,
  issu_istt_cd TEXT,
  etf_chas_erng_rt_dbnb TEXT,
  etf_etn_ivst_heed_item_yn TEXT,
  stln_int_rt_dvsn_cd TEXT,
  frnr_psnl_lmt_rt TEXT,
  lstg_rqsr_issu_istt_cd TEXT,
  lstg_rqsr_item_cd TEXT,
  trst_istt_issu_istt_cd TEXT,
  cptt_trad_tr_psbl_yn TEXT,
  nxt_tr_stop_yn TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_basic_info IS '국내 주식 기본 정보 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_basic_info.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_basic_info.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_basic_info.pdno IS '상품번호';
COMMENT ON COLUMN kr_stock_basic_info.prdt_type_cd IS '상품유형코드';
COMMENT ON COLUMN kr_stock_basic_info.mket_id_cd IS '시장ID코드';
COMMENT ON COLUMN kr_stock_basic_info.scty_grp_id_cd IS '증권그룹ID코드';
COMMENT ON COLUMN kr_stock_basic_info.excg_dvsn_cd IS '거래소구분코드';
COMMENT ON COLUMN kr_stock_basic_info.setl_mmdd IS '결산월일';
COMMENT ON COLUMN kr_stock_basic_info.lstg_stqt IS '상장주수';
COMMENT ON COLUMN kr_stock_basic_info.lstg_cptl_amt IS '상장자본금액';
COMMENT ON COLUMN kr_stock_basic_info.cpta IS '자본금';
COMMENT ON COLUMN kr_stock_basic_info.papr IS '액면가';
COMMENT ON COLUMN kr_stock_basic_info.issu_pric IS '발행가격';
COMMENT ON COLUMN kr_stock_basic_info.kospi200_item_yn IS '코스피200종목여부';
COMMENT ON COLUMN kr_stock_basic_info.scts_mket_lstg_dt IS '유가증권시장상장일자';
COMMENT ON COLUMN kr_stock_basic_info.scts_mket_lstg_abol_dt IS '유가증권시장상장폐지일자';
COMMENT ON COLUMN kr_stock_basic_info.kosdaq_mket_lstg_dt IS '코스닥시장상장일자';
COMMENT ON COLUMN kr_stock_basic_info.kosdaq_mket_lstg_abol_dt IS '코스닥시장상장폐지일자';
COMMENT ON COLUMN kr_stock_basic_info.frbd_mket_lstg_dt IS '프리보드시장상장일자';
COMMENT ON COLUMN kr_stock_basic_info.frbd_mket_lstg_abol_dt IS '프리보드시장상장폐지일자';
COMMENT ON COLUMN kr_stock_basic_info.reits_kind_cd IS '리츠종류코드';
COMMENT ON COLUMN kr_stock_basic_info.etf_dvsn_cd IS 'ETF구분코드';
COMMENT ON COLUMN kr_stock_basic_info.oilf_fund_yn IS '유전펀드여부';
COMMENT ON COLUMN kr_stock_basic_info.idx_bztp_lcls_cd IS '지수업종대분류코드';
COMMENT ON COLUMN kr_stock_basic_info.idx_bztp_mcls_cd IS '지수업종중분류코드';
COMMENT ON COLUMN kr_stock_basic_info.idx_bztp_scls_cd IS '지수업종소분류코드';
COMMENT ON COLUMN kr_stock_basic_info.stck_kind_cd IS '주식종류코드';
COMMENT ON COLUMN kr_stock_basic_info.mfnd_opng_dt IS '뮤추얼펀드개시일자';
COMMENT ON COLUMN kr_stock_basic_info.mfnd_end_dt IS '뮤추얼펀드종료일자';
COMMENT ON COLUMN kr_stock_basic_info.dpsi_erlm_cncl_dt IS '예탁등록취소일자';
COMMENT ON COLUMN kr_stock_basic_info.etf_cu_qty IS 'ETFCU수량';
COMMENT ON COLUMN kr_stock_basic_info.prdt_name IS '상품명';
COMMENT ON COLUMN kr_stock_basic_info.prdt_name120 IS '상품명120';
COMMENT ON COLUMN kr_stock_basic_info.prdt_abrv_name IS '상품약어명';
COMMENT ON COLUMN kr_stock_basic_info.std_pdno IS '표준상품번호';
COMMENT ON COLUMN kr_stock_basic_info.prdt_eng_name IS '상품영문명';
COMMENT ON COLUMN kr_stock_basic_info.prdt_eng_name120 IS '상품영문명120';
COMMENT ON COLUMN kr_stock_basic_info.prdt_eng_abrv_name IS '상품영문약어명';
COMMENT ON COLUMN kr_stock_basic_info.dpsi_aptm_erlm_yn IS '예탁지정등록여부';
COMMENT ON COLUMN kr_stock_basic_info.etf_txtn_type_cd IS 'ETF과세유형코드';
COMMENT ON COLUMN kr_stock_basic_info.etf_type_cd IS 'ETF유형코드';
COMMENT ON COLUMN kr_stock_basic_info.lstg_abol_dt IS '상장폐지일자';
COMMENT ON COLUMN kr_stock_basic_info.nwst_odst_dvsn_cd IS '신주구주구분코드';
COMMENT ON COLUMN kr_stock_basic_info.sbst_pric IS '대용가격';
COMMENT ON COLUMN kr_stock_basic_info.thco_sbst_pric IS '당사대용가격';
COMMENT ON COLUMN kr_stock_basic_info.thco_sbst_pric_chng_dt IS '당사대용가격변경일자';
COMMENT ON COLUMN kr_stock_basic_info.tr_stop_yn IS '거래정지여부';
COMMENT ON COLUMN kr_stock_basic_info.admn_item_yn IS '관리종목여부';
COMMENT ON COLUMN kr_stock_basic_info.thdt_clpr IS '당일종가';
COMMENT ON COLUMN kr_stock_basic_info.bfdy_clpr IS '전일종가';
COMMENT ON COLUMN kr_stock_basic_info.clpr_chng_dt IS '종가변경일자';
COMMENT ON COLUMN kr_stock_basic_info.std_idst_clsf_cd IS '표준산업분류코드';
COMMENT ON COLUMN kr_stock_basic_info.std_idst_clsf_cd_name IS '표준산업분류코드명';
COMMENT ON COLUMN kr_stock_basic_info.idx_bztp_lcls_cd_name IS '지수업종대분류코드명';
COMMENT ON COLUMN kr_stock_basic_info.idx_bztp_mcls_cd_name IS '지수업종중분류코드명';
COMMENT ON COLUMN kr_stock_basic_info.idx_bztp_scls_cd_name IS '지수업종소분류코드명';
COMMENT ON COLUMN kr_stock_basic_info.ocr_no IS 'OCR번호';
COMMENT ON COLUMN kr_stock_basic_info.crfd_item_yn IS '크라우드펀딩종목여부';
COMMENT ON COLUMN kr_stock_basic_info.elec_scty_yn IS '전자증권여부';
COMMENT ON COLUMN kr_stock_basic_info.issu_istt_cd IS '발행기관코드';
COMMENT ON COLUMN kr_stock_basic_info.etf_chas_erng_rt_dbnb IS 'ETF추적수익율배수';
COMMENT ON COLUMN kr_stock_basic_info.etf_etn_ivst_heed_item_yn IS 'ETFETN투자유의종목여부';
COMMENT ON COLUMN kr_stock_basic_info.stln_int_rt_dvsn_cd IS '대주이자율구분코드';
COMMENT ON COLUMN kr_stock_basic_info.frnr_psnl_lmt_rt IS '외국인개인한도비율';
COMMENT ON COLUMN kr_stock_basic_info.lstg_rqsr_issu_istt_cd IS '상장신청인발행기관코드';
COMMENT ON COLUMN kr_stock_basic_info.lstg_rqsr_item_cd IS '상장신청인종목코드';
COMMENT ON COLUMN kr_stock_basic_info.trst_istt_issu_istt_cd IS '신탁기관발행기관코드';
COMMENT ON COLUMN kr_stock_basic_info.cptt_trad_tr_psbl_yn IS 'NXT 거래종목여부';
COMMENT ON COLUMN kr_stock_basic_info.nxt_tr_stop_yn IS 'NXT 거래정지여부';
COMMENT ON COLUMN kr_stock_basic_info.updated_at IS '데이터 마지막 수집 시간';