-- KIS(한국투자증권) API의 "[국내주식] 시세 > 주식현재가 시세"의 데이터를 수집
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_price_basic(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL UNIQUE,
  iscd_stat_cls_code TEXT,
  marg_rate TEXT,
  rprs_mrkt_kor_name TEXT,
  new_hgpr_lwpr_cls_code TEXT,
  bstp_kor_isnm TEXT,
  temp_stop_yn TEXT,
  oprc_rang_cont_yn TEXT,
  clpr_rang_cont_yn TEXT,
  crdt_able_yn TEXT,
  grmn_rate_cls_code TEXT,
  elw_pblc_yn TEXT,
  stck_prpr TEXT,
  prdy_vrss TEXT,
  prdy_vrss_sign TEXT,
  prdy_ctrt TEXT,
  acml_tr_pbmn TEXT,
  acml_vol TEXT,
  prdy_vrss_vol_rate TEXT,
  stck_oprc TEXT,
  stck_hgpr TEXT,
  stck_lwpr TEXT,
  stck_mxpr TEXT,
  stck_llam TEXT,
  stck_sdpr TEXT,
  wghn_avrg_stck_prc TEXT,
  hts_frgn_ehrt TEXT,
  frgn_ntby_qty TEXT,
  pgtr_ntby_qty TEXT,
  pvt_scnd_dmrs_prc TEXT,
  pvt_frst_dmrs_prc TEXT,
  pvt_pont_val TEXT,
  pvt_frst_dmsp_prc TEXT,
  pvt_scnd_dmsp_prc TEXT,
  dmrs_val TEXT,
  dmsp_val TEXT,
  cpfn TEXT,
  rstc_wdth_prc TEXT,
  stck_fcam TEXT,
  stck_sspr TEXT,
  aspr_unit TEXT,
  hts_deal_qty_unit_val TEXT,
  lstn_stcn TEXT,
  hts_avls TEXT,
  per TEXT,
  pbr TEXT,
  stac_month TEXT,
  vol_tnrt TEXT,
  eps TEXT,
  bps TEXT,
  d250_hgpr TEXT,
  d250_hgpr_date TEXT,
  d250_hgpr_vrss_prpr_rate TEXT,
  d250_lwpr TEXT,
  d250_lwpr_date TEXT,
  d250_lwpr_vrss_prpr_rate TEXT,
  stck_dryy_hgpr TEXT,
  dryy_hgpr_vrss_prpr_rate TEXT,
  dryy_hgpr_date TEXT,
  stck_dryy_lwpr TEXT,
  dryy_lwpr_vrss_prpr_rate TEXT,
  dryy_lwpr_date TEXT,
  w52_hgpr TEXT,
  w52_hgpr_vrss_prpr_ctrt TEXT,
  w52_hgpr_date TEXT,
  w52_lwpr TEXT,
  w52_lwpr_vrss_prpr_ctrt TEXT,
  w52_lwpr_date TEXT,
  whol_loan_rmnd_rate TEXT,
  ssts_yn TEXT,
  stck_shrn_iscd TEXT,
  fcam_cnnm TEXT,
  cpfn_cnnm TEXT,
  apprch_rate TEXT,
  frgn_hldn_qty TEXT,
  vi_cls_code TEXT,
  ovtm_vi_cls_code TEXT,
  last_ssts_cntg_qty TEXT,
  invt_caful_yn TEXT,
  mrkt_warn_cls_code TEXT,
  short_over_yn TEXT,
  sltr_yn TEXT,
  mang_issu_cls_code TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_price_basic IS '국내 주식 현재가 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_price_basic.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_price_basic.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_price_basic.iscd_stat_cls_code IS '종목 상태 구분 코드';
COMMENT ON COLUMN kr_stock_price_basic.marg_rate IS '증거금 비율';
COMMENT ON COLUMN kr_stock_price_basic.rprs_mrkt_kor_name IS '대표 시장 한글 명';
COMMENT ON COLUMN kr_stock_price_basic.new_hgpr_lwpr_cls_code IS '신 고가 저가 구분 코드';
COMMENT ON COLUMN kr_stock_price_basic.bstp_kor_isnm IS '업종 한글 종목명';
COMMENT ON COLUMN kr_stock_price_basic.temp_stop_yn IS '임시 정지 여부';
COMMENT ON COLUMN kr_stock_price_basic.oprc_rang_cont_yn IS '시가 범위 연장 여부';
COMMENT ON COLUMN kr_stock_price_basic.clpr_rang_cont_yn IS '종가 범위 연장 여부';
COMMENT ON COLUMN kr_stock_price_basic.crdt_able_yn IS '신용 가능 여부';
COMMENT ON COLUMN kr_stock_price_basic.grmn_rate_cls_code IS '보증금 비율 구분 코드';
COMMENT ON COLUMN kr_stock_price_basic.elw_pblc_yn IS 'ELW 발행 여부';
COMMENT ON COLUMN kr_stock_price_basic.stck_prpr IS '주식 현재가';
COMMENT ON COLUMN kr_stock_price_basic.prdy_vrss IS '전일 대비';
COMMENT ON COLUMN kr_stock_price_basic.prdy_vrss_sign IS '전일 대비 부호';
COMMENT ON COLUMN kr_stock_price_basic.prdy_ctrt IS '전일 대비율';
COMMENT ON COLUMN kr_stock_price_basic.acml_tr_pbmn IS '누적 거래 대금';
COMMENT ON COLUMN kr_stock_price_basic.acml_vol IS '누적 거래량';
COMMENT ON COLUMN kr_stock_price_basic.prdy_vrss_vol_rate IS '전일 대비 거래량 비율';
COMMENT ON COLUMN kr_stock_price_basic.stck_oprc IS '주식 시가';
COMMENT ON COLUMN kr_stock_price_basic.stck_hgpr IS '주식 최고가';
COMMENT ON COLUMN kr_stock_price_basic.stck_lwpr IS '주식 최저가';
COMMENT ON COLUMN kr_stock_price_basic.stck_mxpr IS '주식 상한가';
COMMENT ON COLUMN kr_stock_price_basic.stck_llam IS '주식 하한가';
COMMENT ON COLUMN kr_stock_price_basic.stck_sdpr IS '주식 기준가';
COMMENT ON COLUMN kr_stock_price_basic.wghn_avrg_stck_prc IS '가중 평균 주식 가격';
COMMENT ON COLUMN kr_stock_price_basic.hts_frgn_ehrt IS 'HTS 외국인 소진율';
COMMENT ON COLUMN kr_stock_price_basic.frgn_ntby_qty IS '외국인 순매수 수량';
COMMENT ON COLUMN kr_stock_price_basic.pgtr_ntby_qty IS '프로그램매매 순매수 수량';
COMMENT ON COLUMN kr_stock_price_basic.pvt_scnd_dmrs_prc IS '피벗 2차 디저항 가격';
COMMENT ON COLUMN kr_stock_price_basic.pvt_frst_dmrs_prc IS '피벗 1차 디저항 가격';
COMMENT ON COLUMN kr_stock_price_basic.pvt_pont_val IS '피벗 포인트 값';
COMMENT ON COLUMN kr_stock_price_basic.pvt_frst_dmsp_prc IS '피벗 1차 디지지 가격';
COMMENT ON COLUMN kr_stock_price_basic.pvt_scnd_dmsp_prc IS '피벗 2차 디지지 가격';
COMMENT ON COLUMN kr_stock_price_basic.dmrs_val IS '디저항 값';
COMMENT ON COLUMN kr_stock_price_basic.dmsp_val IS '디지지 값';
COMMENT ON COLUMN kr_stock_price_basic.cpfn IS '자본금';
COMMENT ON COLUMN kr_stock_price_basic.rstc_wdth_prc IS '제한 폭 가격';
COMMENT ON COLUMN kr_stock_price_basic.stck_fcam IS '주식 액면가';
COMMENT ON COLUMN kr_stock_price_basic.stck_sspr IS '주식 대용가';
COMMENT ON COLUMN kr_stock_price_basic.aspr_unit IS '호가단위';
COMMENT ON COLUMN kr_stock_price_basic.hts_deal_qty_unit_val IS 'HTS 매매 수량 단위 값';
COMMENT ON COLUMN kr_stock_price_basic.lstn_stcn IS '상장 주수';
COMMENT ON COLUMN kr_stock_price_basic.hts_avls IS 'HTS 시가총액';
COMMENT ON COLUMN kr_stock_price_basic.per IS 'PER';
COMMENT ON COLUMN kr_stock_price_basic.pbr IS 'PBR';
COMMENT ON COLUMN kr_stock_price_basic.stac_month IS '결산 월';
COMMENT ON COLUMN kr_stock_price_basic.vol_tnrt IS '거래량 회전율';
COMMENT ON COLUMN kr_stock_price_basic.eps IS 'EPS';
COMMENT ON COLUMN kr_stock_price_basic.bps IS 'BPS';
COMMENT ON COLUMN kr_stock_price_basic.d250_hgpr IS '250일 최고가';
COMMENT ON COLUMN kr_stock_price_basic.d250_hgpr_date IS '250일 최고가 일자';
COMMENT ON COLUMN kr_stock_price_basic.d250_hgpr_vrss_prpr_rate IS '250일 최고가 대비 현재가 비율';
COMMENT ON COLUMN kr_stock_price_basic.d250_lwpr IS '250일 최저가';
COMMENT ON COLUMN kr_stock_price_basic.d250_lwpr_date IS '250일 최저가 일자';
COMMENT ON COLUMN kr_stock_price_basic.d250_lwpr_vrss_prpr_rate IS '250일 최저가 대비 현재가 비율';
COMMENT ON COLUMN kr_stock_price_basic.stck_dryy_hgpr IS '주식 연중 최고가';
COMMENT ON COLUMN kr_stock_price_basic.dryy_hgpr_vrss_prpr_rate IS '연중 최고가 대비 현재가 비율';
COMMENT ON COLUMN kr_stock_price_basic.dryy_hgpr_date IS '연중 최고가 일자';
COMMENT ON COLUMN kr_stock_price_basic.stck_dryy_lwpr IS '주식 연중 최저가';
COMMENT ON COLUMN kr_stock_price_basic.dryy_lwpr_vrss_prpr_rate IS '연중 최저가 대비 현재가 비율';
COMMENT ON COLUMN kr_stock_price_basic.dryy_lwpr_date IS '연중 최저가 일자';
COMMENT ON COLUMN kr_stock_price_basic.w52_hgpr IS '52주일 최고가';
COMMENT ON COLUMN kr_stock_price_basic.w52_hgpr_vrss_prpr_ctrt IS '52주일 최고가 대비 현재가 대비';
COMMENT ON COLUMN kr_stock_price_basic.w52_hgpr_date IS '52주일 최고가 일자';
COMMENT ON COLUMN kr_stock_price_basic.w52_lwpr IS '52주일 최저가';
COMMENT ON COLUMN kr_stock_price_basic.w52_lwpr_vrss_prpr_ctrt IS '52주일 최저가 대비 현재가 대비';
COMMENT ON COLUMN kr_stock_price_basic.w52_lwpr_date IS '52주일 최저가 일자';
COMMENT ON COLUMN kr_stock_price_basic.whol_loan_rmnd_rate IS '전체 융자 잔고 비율';
COMMENT ON COLUMN kr_stock_price_basic.ssts_yn IS '공매도가능여부';
COMMENT ON COLUMN kr_stock_price_basic.stck_shrn_iscd IS '주식 단축 종목코드';
COMMENT ON COLUMN kr_stock_price_basic.fcam_cnnm IS '액면가 통화명';
COMMENT ON COLUMN kr_stock_price_basic.cpfn_cnnm IS '자본금 통화명';
COMMENT ON COLUMN kr_stock_price_basic.apprch_rate IS '접근도';
COMMENT ON COLUMN kr_stock_price_basic.frgn_hldn_qty IS '외국인 보유 수량';
COMMENT ON COLUMN kr_stock_price_basic.vi_cls_code IS 'VI적용구분코드';
COMMENT ON COLUMN kr_stock_price_basic.ovtm_vi_cls_code IS '시간외단일가VI적용구분코드';
COMMENT ON COLUMN kr_stock_price_basic.last_ssts_cntg_qty IS '최종 공매도 체결 수량';
COMMENT ON COLUMN kr_stock_price_basic.invt_caful_yn IS '투자유의여부';
COMMENT ON COLUMN kr_stock_price_basic.mrkt_warn_cls_code IS '시장경고코드';
COMMENT ON COLUMN kr_stock_price_basic.short_over_yn IS '단기과열여부';
COMMENT ON COLUMN kr_stock_price_basic.sltr_yn IS '정리매매여부';
COMMENT ON COLUMN kr_stock_price_basic.mang_issu_cls_code IS '관리종목여부';
COMMENT ON COLUMN kr_stock_price_basic.updated_at IS '데이터 마지막 수집 시간';