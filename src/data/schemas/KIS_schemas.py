from dataclasses import dataclass

@dataclass
class KrStockBasicInfo: # 국내 주식 종목 기본 정보
  pdno: str    #상품번호
  prdt_type_cd: str    #상품유형코드
  mket_id_cd: str    #시장ID코드
  scty_grp_id_cd: str    #증권그룹ID코드
  excg_dvsn_cd: str    #거래소구분코드
  setl_mmdd: str    #결산월일
  lstg_stqt: str    #상장주수
  lstg_cptl_amt: str    #상장자본금액
  cpta: str    #자본금
  papr: str    #액면가
  issu_pric: str    #발행가격
  kospi200_item_yn: str    #코스피200종목여부
  scts_mket_lstg_dt: str    #유가증권시장상장일자
  scts_mket_lstg_abol_dt: str    #유가증권시장상장폐지일자
  kosdaq_mket_lstg_dt: str    #코스닥시장상장일자
  kosdaq_mket_lstg_abol_dt: str    #코스닥시장상장폐지일자
  frbd_mket_lstg_dt: str    #프리보드시장상장일자
  frbd_mket_lstg_abol_dt: str    #프리보드시장상장폐지일자
  reits_kind_cd: str    #리츠종류코드
  etf_dvsn_cd: str    #ETF구분코드
  oilf_fund_yn: str    #유전펀드여부
  idx_bztp_lcls_cd: str    #지수업종대분류코드
  idx_bztp_mcls_cd: str    #지수업종중분류코드
  idx_bztp_scls_cd: str    #지수업종소분류코드
  stck_kind_cd: str    #주식종류코드
  mfnd_opng_dt: str    #뮤추얼펀드개시일자
  mfnd_end_dt: str    #뮤추얼펀드종료일자
  dpsi_erlm_cncl_dt: str    #예탁등록취소일자
  etf_cu_qty: str    #ETFCU수량
  prdt_name: str    #상품명
  prdt_name120: str    #상품명120
  prdt_abrv_name: str    #상품약어명
  std_pdno: str    #표준상품번호
  prdt_eng_name: str    #상품영문명
  prdt_eng_name120: str    #상품영문명120
  prdt_eng_abrv_name: str    #상품영문약어명
  dpsi_aptm_erlm_yn: str    #예탁지정등록여부
  etf_txtn_type_cd: str    #ETF과세유형코드
  etf_type_cd: str    #ETF유형코드
  lstg_abol_dt: str    #상장폐지일자
  nwst_odst_dvsn_cd: str    #신주구주구분코드
  sbst_pric: str    #대용가격
  thco_sbst_pric: str    #당사대용가격
  thco_sbst_pric_chng_dt: str    #당사대용가격변경일자
  tr_stop_yn: str    #거래정지여부
  admn_item_yn: str    #관리종목여부
  thdt_clpr: str    #당일종가
  bfdy_clpr: str    #전일종가
  clpr_chng_dt: str    #종가변경일자
  std_idst_clsf_cd: str    #표준산업분류코드
  std_idst_clsf_cd_name: str    #표준산업분류코드명
  idx_bztp_lcls_cd_name: str    #지수업종대분류코드명
  idx_bztp_mcls_cd_name: str    #지수업종중분류코드명
  idx_bztp_scls_cd_name: str    #지수업종소분류코드명
  ocr_no: str    #OCR번호
  crfd_item_yn: str    #크라우드펀딩종목여부
  elec_scty_yn: str    #전자증권여부
  issu_istt_cd: str    #발행기관코드
  etf_chas_erng_rt_dbnb: str    #ETF추적수익율배수
  etf_etn_ivst_heed_item_yn: str    #ETFETN투자유의종목여부
  stln_int_rt_dvsn_cd: str    #대주이자율구분코드
  frnr_psnl_lmt_rt: str    #외국인개인한도비율
  lstg_rqsr_issu_istt_cd: str    #상장신청인발행기관코드
  lstg_rqsr_item_cd: str    #상장신청인종목코드
  trst_istt_issu_istt_cd: str    #신탁기관발행기관코드
  cptt_trad_tr_psbl_yn: str    #NXT 거래종목여부
  nxt_tr_stop_yn: str    #NXT 거래정지여부

@dataclass
class KrStockBalanceSheet: # 국내 주식 대차대조표
  stac_yymm: str    #결산 년월
  cras: str    #유동자산
  fxas: str    #고정자산
  total_aset: str    #자산총계
  flow_lblt: str    #유동부채
  fix_lblt: str    #고정부채
  total_lblt: str    #부채총계
  cpfn: str    #자본금
  cfp_surp: str    #자본 잉여금
  prfi_surp: str    #이익 잉여금
  total_cptl: str    #자본총계

@dataclass
class KrStockIncomeStatement: # 국내 주식 손익계산서
  stac_yymm: str    #결산 년월
  sale_account: str    #매출액
  sale_cost: str    #매출 원가
  sale_totl_prfi: str    #매출 총 이익
  depr_cost: str    #감가상각비
  sell_mang: str    #판매 및 관리비
  bsop_prti: str    #영업 이익
  bsop_non_ernn: str    #영업 외 수익
  bsop_non_expn: str    #영업 외 비용
  op_prfi: str    #경상 이익
  spec_prfi: str    #특별 이익
  spec_loss: str    #특별 손실
  thtr_ntin: str    #당기순이익  

@dataclass
class KrStockFinancialRatio: # 국내 주식 재무비율
  stac_yymm: str    #결산 년월
  grs: str    #매출액 증가율
  bsop_prfi_inrt: str    #영업 이익 증가율
  ntin_inrt: str    #순이익 증가율
  roe_val: str    #ROE 값
  eps: str    #EPS
  sps: str    #주당매출액
  bps: str    #BPS
  rsrv_rate: str    #유보 비율
  lblt_rate: str    #부채 비율


@dataclass
class KrStockProfitRatio: # 국내 주식 수익성비율
  stac_yymm: str    #결산 년월
  cptl_ntin_rate: str    #총자본 순이익율
  self_cptl_ntin_inrt: str    #자기자본 순이익율
  sale_ntin_rate: str    #매출액 순이익율
  sale_totl_rate: str    #매출액 총이익율

@dataclass
class KrStockOtherMajorRatio: # 국내 주식 기타 주요비율
  stac_yymm: str    #결산 년월
  payout_rate: str    #배당 성향
  eva: str    #EVA
  ebitda: str    #EBITDA
  ev_ebitda: str    #EV_EBITDA

@dataclass
class KrStockStabilityRatio: # 국내 주식 안정성비율
  stac_yymm: str    #결산 년월
  lblt_rate: str    #부채 비율
  bram_depn: str    #차입금 의존도
  crnt_rate: str    #유동 비율
  quck_rate: str    #당좌 비율

@dataclass
class KrStockGrowthRatio: # 국내 주식 성장성비율
  stac_yymm: str    #결산 년월
  grs: str    #매출액 증가율
  bsop_prfi_inrt: str    #영업 이익 증가율
  equt_inrt: str    #자기자본 증가율
  totl_aset_inrt: str    #총자산 증가율

@dataclass
class KrStockDividend:
  record_date: str    #기준일
  sht_cd: str    #종목코드
  isin_name: str    #종목명
  divi_kind: str    #배당종류
  face_val: str    #액면가
  per_sto_divi_amt: str    #현금배당금
  divi_rate: str    #현금배당률(%)
  stk_divi_rate: str    #주식배당률(%)
  divi_pay_dt: str    #배당금지급일
  stk_div_pay_dt: str    #주식배당지급일
  odd_pay_dt: str    #단주대금지급일
  stk_kind: str    #주식종류
  high_divi_gb: str    #고배당종목여부

@dataclass
class KrStockEstimatePerform:
  sht_cd: str    #ELW단축종목코드
  item_kor_nm: str    #HTS한글종목명
  name1: str    #ELW현재가
  name2: str    #전일대비
  estdate: str    #전일대비부호
  rcmd_name: str    #전일대비율
  capital: str    #누적거래량
  forn_item_lmtrt: str    #행사가

from dataclasses import dataclass

@dataclass
class KrStockEstimatePerform:
  # 기본 정보
  ticker: str                     # 종목코드
  period: str                     # 실적 기준 기간 (예: 2022.12E)
  analyst: str                    # 담당 애널리스트
  opinion: str                    # 투자의견
  # 성장성 지표
  revenue: float                  # 매출액
  revenue_yoy: float              # 매출액 증감률 (YoY: Year-on-Year)
  operating_profit: float         # 영업이익
  operating_profit_yoy: float     # 영업이익 증감률 (YoY)
  net_income: float               # 당기순이익
  net_income_yoy: float           # 당기순이익 증감률 (YoY)
  # 주당 가치 지표
  eps: float                      # EPS (Earning Per Share): 주당순이익
  eps_yoy: float                  # EPS 증감률 (YoY)
  bps: float                      # BPS (Book-value Per Share): 주당순자산가치
  # 가치평가(Valuation) 지표
  per: float                      # PER (Price Earning Ratio): 주가수익비율
  pbr: float                      # PBR (Price Book-value Ratio): 주가순자산비율
  psr: float                      # PSR (Price Selling Ratio): 주가매출비율
  # 수익성 및 효율성 지표
  roe: float                      # ROE (Return On Equity): 자기자본이익률
  ebitda: float                   # EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization): 법인세 이자 감가상각비 차감 전 영업이익
  ev_ebitda: float                # EV/EBITDA (Enterprise Value to EBITDA): 기업가치를 EBITDA로 나눈 값
  # 안정성 지표
  debt_ratio: float               # 부채비율
  interest_coverage_ratio: float  # 이자보상배율

@dataclass
class KrStockInvestOpinion:
  stck_bsop_date: str    #주식영업일자
  invt_opnn: str    #투자의견
  invt_opnn_cls_code: str    #투자의견구분코드
  rgbf_invt_opnn: str    #직전투자의견
  rgbf_invt_opnn_cls_code: str    #직전투자의견구분코드
  mbcr_name: str    #회원사명
  hts_goal_prc: str    #HTS목표가격
  stck_prdy_clpr: str    #주식전일종가
  stck_nday_esdg: str    #주식N일괴리도
  nday_dprt: str    #N일괴리율
  stft_esdg: str    #주식선물괴리도
  dprt: str    #괴리율

@dataclass
class KrStockInvestOpbysec:
  stck_bsop_date: str    #주식영업일자
  stck_shrn_iscd: str    #주식단축종목코드
  hts_kor_isnm: str    #HTS한글종목명
  invt_opnn: str    #투자의견
  invt_opnn_cls_code: str    #투자의견구분코드
  rgbf_invt_opnn: str    #직전투자의견
  rgbf_invt_opnn_cls_code: str    #직전투자의견구분코드
  mbcr_name: str    #회원사명
  stck_prpr: str    #주식현재가
  prdy_vrss: str    #전일대비
  prdy_vrss_sign: str    #전일대비부호
  prdy_ctrt: str    #전일대비율
  hts_goal_prc: str    #HTS목표가격
  stck_prdy_clpr: str    #주식전일종가
  stft_esdg: str    #주식선물괴리도
  dprt: str    #괴리율

@dataclass
class KrStockPriceBasic:
  iscd_stat_cls_code: str    #종목 상태 구분 코드
  marg_rate: str    #증거금 비율
  rprs_mrkt_kor_name: str    #대표 시장 한글 명
  new_hgpr_lwpr_cls_code: str    #신 고가 저가 구분 코드
  bstp_kor_isnm: str    #업종 한글 종목명
  temp_stop_yn: str    #임시 정지 여부
  oprc_rang_cont_yn: str    #시가 범위 연장 여부
  clpr_rang_cont_yn: str    #종가 범위 연장 여부
  crdt_able_yn: str    #신용 가능 여부
  grmn_rate_cls_code: str    #보증금 비율 구분 코드
  elw_pblc_yn: str    #ELW 발행 여부
  stck_prpr: str    #주식 현재가
  prdy_vrss: str    #전일 대비
  prdy_vrss_sign: str    #전일 대비 부호
  prdy_ctrt: str    #전일 대비율
  acml_tr_pbmn: str    #누적 거래 대금
  acml_vol: str    #누적 거래량
  prdy_vrss_vol_rate: str    #전일 대비 거래량 비율
  stck_oprc: str    #주식 시가2
  stck_hgpr: str    #주식 최고가
  stck_lwpr: str    #주식 최저가
  stck_mxpr: str    #주식 상한가
  stck_llam: str    #주식 하한가
  stck_sdpr: str    #주식 기준가
  wghn_avrg_stck_prc: str    #가중 평균 주식 가격
  hts_frgn_ehrt: str    #HTS 외국인 소진율
  frgn_ntby_qty: str    #외국인 순매수 수량
  pgtr_ntby_qty: str    #프로그램매매 순매수 수량
  pvt_scnd_dmrs_prc: str    #피벗 2차 디저항 가격
  pvt_frst_dmrs_prc: str    #피벗 1차 디저항 가격
  pvt_pont_val: str    #피벗 포인트 값
  pvt_frst_dmsp_prc: str    #피벗 1차 디지지 가격
  pvt_scnd_dmsp_prc: str    #피벗 2차 디지지 가격
  dmrs_val: str    #디저항 값
  dmsp_val: str    #디지지 값
  cpfn: str    #자본금
  rstc_wdth_prc: str    #제한 폭 가격
  stck_fcam: str    #주식 액면가
  stck_sspr: str    #주식 대용가
  aspr_unit: str    #호가단위
  hts_deal_qty_unit_val: str    #HTS 매매 수량 단위 값
  lstn_stcn: str    #상장 주수
  hts_avls: str    #HTS 시가총액
  per: str    #PER
  pbr: str    #PBR
  stac_month: str    #결산 월
  vol_tnrt: str    #거래량 회전율
  eps: str    #EPS
  bps: str    #BPS
  d250_hgpr: str    #250일 최고가
  d250_hgpr_date: str    #250일 최고가 일자
  d250_hgpr_vrss_prpr_rate: str    #250일 최고가 대비 현재가 비율
  d250_lwpr: str    #250일 최저가
  d250_lwpr_date: str    #250일 최저가 일자
  d250_lwpr_vrss_prpr_rate: str    #250일 최저가 대비 현재가 비율
  stck_dryy_hgpr: str    #주식 연중 최고가
  dryy_hgpr_vrss_prpr_rate: str    #연중 최고가 대비 현재가 비율
  dryy_hgpr_date: str    #연중 최고가 일자
  stck_dryy_lwpr: str    #주식 연중 최저가
  dryy_lwpr_vrss_prpr_rate: str    #연중 최저가 대비 현재가 비율
  dryy_lwpr_date: str    #연중 최저가 일자
  w52_hgpr: str    #52주일 최고가
  w52_hgpr_vrss_prpr_ctrt: str    #52주일 최고가 대비 현재가 대비
  w52_hgpr_date: str    #52주일 최고가 일자
  w52_lwpr: str    #52주일 최저가
  w52_lwpr_vrss_prpr_ctrt: str    #52주일 최저가 대비 현재가 대비
  w52_lwpr_date: str    #52주일 최저가 일자
  whol_loan_rmnd_rate: str    #전체 융자 잔고 비율
  ssts_yn: str    #공매도가능여부
  stck_shrn_iscd: str    #주식 단축 종목코드
  fcam_cnnm: str    #액면가 통화명
  cpfn_cnnm: str    #자본금 통화명
  apprch_rate: str    #접근도
  frgn_hldn_qty: str    #외국인 보유 수량
  vi_cls_code: str    #VI적용구분코드
  ovtm_vi_cls_code: str    #시간외단일가VI적용구분코드
  last_ssts_cntg_qty: str    #최종 공매도 체결 수량
  invt_caful_yn: str    #투자유의여부
  mrkt_warn_cls_code: str    #시장경고코드
  short_over_yn: str    #단기과열여부
  sltr_yn: str    #정리매매여부
  mang_issu_cls_code: str    #관리종목여부

@dataclass
class KrStockPriceDetail:
  rprs_mrkt_kor_name: str    #대표 시장 한글 명
  new_hgpr_lwpr_cls_code: str    #신 고가 저가 구분 코드
  mxpr_llam_cls_code: str    #상하한가 구분 코드
  crdt_able_yn: str    #신용 가능 여부
  stck_mxpr: str    #주식 상한가
  elw_pblc_yn: str    #ELW 발행 여부
  prdy_clpr_vrss_oprc_rate: str    #전일 종가 대비 시가2 비율
  crdt_rate: str    #신용 비율
  marg_rate: str    #증거금 비율
  lwpr_vrss_prpr: str    #최저가 대비 현재가
  lwpr_vrss_prpr_sign: str    #최저가 대비 현재가 부호
  prdy_clpr_vrss_lwpr_rate: str    #전일 종가 대비 최저가 비율
  stck_lwpr: str    #주식 최저가
  hgpr_vrss_prpr: str    #최고가 대비 현재가
  hgpr_vrss_prpr_sign: str    #최고가 대비 현재가 부호
  prdy_clpr_vrss_hgpr_rate: str    #전일 종가 대비 최고가 비율
  stck_hgpr: str    #주식 최고가
  oprc_vrss_prpr: str    #시가2 대비 현재가
  oprc_vrss_prpr_sign: str    #시가2 대비 현재가 부호
  mang_issu_yn: str    #관리 종목 여부
  divi_app_cls_code: str    #동시호가배분처리코드
  short_over_yn: str    #단기과열여부
  mrkt_warn_cls_code: str    #시장경고코드
  invt_caful_yn: str    #투자유의여부
  stange_runup_yn: str    #이상급등여부
  ssts_hot_yn: str    #공매도과열 여부
  low_current_yn: str    #저유동성 종목 여부
  vi_cls_code: str    #VI적용구분코드
  short_over_cls_code: str    #단기과열구분코드
  stck_llam: str    #주식 하한가
  new_lstn_cls_name: str    #신규 상장 구분 명
  vlnt_deal_cls_name: str    #임의 매매 구분 명
  flng_cls_name: str    #락 구분 이름
  revl_issu_reas_name: str    #재평가 종목 사유 명
  mrkt_warn_cls_name: str    #시장 경고 구분 명
  stck_sdpr: str    #주식 기준가
  bstp_cls_code: str    #업종 구분 코드
  stck_prdy_clpr: str    #주식 전일 종가
  insn_pbnt_yn: str    #불성실 공시 여부
  fcam_mod_cls_name: str    #액면가 변경 구분 명
  stck_prpr: str    #주식 현재가
  prdy_vrss: str    #전일 대비
  prdy_vrss_sign: str    #전일 대비 부호
  prdy_ctrt: str    #전일 대비율
  acml_tr_pbmn: str    #누적 거래 대금
  acml_vol: str    #누적 거래량
  prdy_vrss_vol_rate: str    #전일 대비 거래량 비율
  bstp_kor_isnm: str    #업종 한글 종목명
  sltr_yn: str    #정리매매 여부
  trht_yn: str    #거래정지 여부
  oprc_rang_cont_yn: str    #시가 범위 연장 여부
  vlnt_fin_cls_code: str    #임의 종료 구분 코드
  stck_oprc: str    #주식 시가2
  prdy_vol: str    #전일 거래량

from dataclasses import dataclass

@dataclass
class KrStockAskingPrice:
  ticker: str    # 종목코드
  aspr_acpt_hour: str    # 호가 접수 시간
  askp1: str    # 매도호가1
  askp2: str    # 매도호가2
  askp3: str    # 매도호가3
  askp4: str    # 매도호가4
  askp5: str    # 매도호가5
  askp6: str    # 매도호가6
  askp7: str    # 매도호가7
  askp8: str    # 매도호가8
  askp9: str    # 매도호가9
  askp10: str    # 매도호가10
  bidp1: str    # 매수호가1
  bidp2: str    # 매수호가2
  bidp3: str    # 매수호가3
  bidp4: str    # 매수호가4
  bidp5: str    # 매수호가5
  bidp6: str    # 매수호가6
  bidp7: str    # 매수호가7
  bidp8: str    # 매수호가8
  bidp9: str    # 매수호가9
  bidp10: str    # 매수호가10
  askp_rsqn1: str    # 매도호가 잔량1
  askp_rsqn2: str    # 매도호가 잔량2
  askp_rsqn3: str    # 매도호가 잔량3
  askp_rsqn4: str    # 매도호가 잔량4
  askp_rsqn5: str    # 매도호가 잔량5
  askp_rsqn6: str    # 매도호가 잔량6
  askp_rsqn7: str    # 매도호가 잔량7
  askp_rsqn8: str    # 매도호가 잔량8
  askp_rsqn9: str    # 매도호가 잔량9
  askp_rsqn10: str    # 매도호가 잔량10
  bidp_rsqn1: str    # 매수호가 잔량1
  bidp_rsqn2: str    # 매수호가 잔량2
  bidp_rsqn3: str    # 매수호가 잔량3
  bidp_rsqn4: str    # 매수호가 잔량4
  bidp_rsqn5: str    # 매수호가 잔량5
  bidp_rsqn6: str    # 매수호가 잔량6
  bidp_rsqn7: str    # 매수호가 잔량7
  bidp_rsqn8: str    # 매수호가 잔량8
  bidp_rsqn9: str    # 매수호가 잔량9
  bidp_rsqn10: str    # 매수호가 잔량10
  askp_rsqn_icdc1: str    # 매도호가 잔량 증감1
  askp_rsqn_icdc2: str    # 매도호가 잔량 증감2
  askp_rsqn_icdc3: str    # 매도호가 잔량 증감3
  askp_rsqn_icdc4: str    # 매도호가 잔량 증감4
  askp_rsqn_icdc5: str    # 매도호가 잔량 증감5
  askp_rsqn_icdc6: str    # 매도호가 잔량 증감6
  askp_rsqn_icdc7: str    # 매도호가 잔량 증감7
  askp_rsqn_icdc8: str    # 매도호가 잔량 증감8
  askp_rsqn_icdc9: str    # 매도호가 잔량 증감9
  askp_rsqn_icdc10: str    # 매도호가 잔량 증감10
  bidp_rsqn_icdc1: str    # 매수호가 잔량 증감1
  bidp_rsqn_icdc2: str    # 매수호가 잔량 증감2
  bidp_rsqn_icdc3: str    # 매수호가 잔량 증감3
  bidp_rsqn_icdc4: str    # 매수호가 잔량 증감4
  bidp_rsqn_icdc5: str    # 매수호가 잔량 증감5
  bidp_rsqn_icdc6: str    # 매수호가 잔량 증감6
  bidp_rsqn_icdc7: str    # 매수호가 잔량 증감7
  bidp_rsqn_icdc8: str    # 매수호가 잔량 증감8
  bidp_rsqn_icdc9: str    # 매수호가 잔량 증감9
  bidp_rsqn_icdc10: str    # 매수호가 잔량 증감10
  total_askp_rsqn: str    # 총 매도호가 잔량
  total_bidp_rsqn: str    # 총 매수호가 잔량
  total_askp_rsqn_icdc: str    # 총 매도호가 잔량 증감
  total_bidp_rsqn_icdc: str    # 총 매수호가 잔량 증감
  ovtm_total_askp_icdc: str    # 시간외 총 매도호가 증감
  ovtm_total_bidp_icdc: str    # 시간외 총 매수호가 증감
  ovtm_total_askp_rsqn: str    # 시간외 총 매도호가 잔량
  ovtm_total_bidp_rsqn: str    # 시간외 총 매수호가 잔량
  ntby_aspr_rsqn: str    # 순매수 호가 잔량
  new_mkop_cls_code: str    # 신 장운영 구분 코드
  antc_mkop_cls_code: str    # 예상 장운영 구분 코드
  stck_prpr: str    # 주식 현재가
  stck_oprc: str    # 주식 시가2
  stck_hgpr: str    # 주식 최고가
  stck_lwpr: str    # 주식 최저가
  stck_sdpr: str    # 주식 기준가
  antc_cnpr: str    # 예상 체결가
  antc_cntg_vrss_sign: str    # 예상 체결 대비 부호
  antc_cntg_vrss: str    # 예상 체결 대비
  antc_cntg_prdy_ctrt: str    # 예상 체결 전일 대비율
  antc_vol: str    # 예상 거래량
  stck_shrn_iscd: str    # 주식 단축 종목코드
  vi_cls_code: str    # VI적용구분코드

@dataclass
class KrStockInvestor:
  stck_bsop_date: str    #주식 영업 일자
  stck_clpr: str    #주식 종가
  prdy_vrss: str    #전일 대비
  prdy_vrss_sign: str    #전일 대비 부호
  prsn_ntby_qty: str    #개인 순매수 수량
  frgn_ntby_qty: str    #외국인 순매수 수량
  orgn_ntby_qty: str    #기관계 순매수 수량
  prsn_ntby_tr_pbmn: str    #개인 순매수 거래 대금
  frgn_ntby_tr_pbmn: str    #외국인 순매수 거래 대금
  orgn_ntby_tr_pbmn: str    #기관계 순매수 거래 대금
  prsn_shnu_vol: str    #개인 매수2 거래량
  frgn_shnu_vol: str    #외국인 매수2 거래량
  orgn_shnu_vol: str    #기관계 매수2 거래량
  prsn_shnu_tr_pbmn: str    #개인 매수2 거래 대금
  frgn_shnu_tr_pbmn: str    #외국인 매수2 거래 대금
  orgn_shnu_tr_pbmn: str    #기관계 매수2 거래 대금
  prsn_seln_vol: str    #개인 매도 거래량
  frgn_seln_vol: str    #외국인 매도 거래량
  orgn_seln_vol: str    #기관계 매도 거래량
  prsn_seln_tr_pbmn: str    #개인 매도 거래 대금
  frgn_seln_tr_pbmn: str    #외국인 매도 거래 대금
  orgn_seln_tr_pbmn: str    #기관계 매도 거래 대금

@dataclass
class KrStockMember:
  seln_mbcr_no1: str    #매도 회원사 번호1
  seln_mbcr_no2: str    #매도 회원사 번호2
  seln_mbcr_no3: str    #매도 회원사 번호3
  seln_mbcr_no4: str    #매도 회원사 번호4
  seln_mbcr_no5: str    #매도 회원사 번호5
  seln_mbcr_name1: str    #매도 회원사 명1
  seln_mbcr_name2: str    #매도 회원사 명2
  seln_mbcr_name3: str    #매도 회원사 명3
  seln_mbcr_name4: str    #매도 회원사 명4
  seln_mbcr_name5: str    #매도 회원사 명5
  total_seln_qty1: str    #총 매도 수량1
  total_seln_qty2: str    #총 매도 수량2
  total_seln_qty3: str    #총 매도 수량3
  total_seln_qty4: str    #총 매도 수량4
  total_seln_qty5: str    #총 매도 수량5
  seln_mbcr_rlim1: str    #매도 회원사 비중1
  seln_mbcr_rlim2: str    #매도 회원사 비중2
  seln_mbcr_rlim3: str    #매도 회원사 비중3
  seln_mbcr_rlim4: str    #매도 회원사 비중4
  seln_mbcr_rlim5: str    #매도 회원사 비중5
  seln_qty_icdc1: str    #매도 수량 증감1
  seln_qty_icdc2: str    #매도 수량 증감2
  seln_qty_icdc3: str    #매도 수량 증감3
  seln_qty_icdc4: str    #매도 수량 증감4
  seln_qty_icdc5: str    #매도 수량 증감5
  shnu_mbcr_no1: str    #매수2 회원사 번호1
  shnu_mbcr_no2: str    #매수2 회원사 번호2
  shnu_mbcr_no3: str    #매수2 회원사 번호3
  shnu_mbcr_no4: str    #매수2 회원사 번호4
  shnu_mbcr_no5: str    #매수2 회원사 번호5
  shnu_mbcr_name1: str    #매수2 회원사 명1
  shnu_mbcr_name2: str    #매수2 회원사 명2
  shnu_mbcr_name3: str    #매수2 회원사 명3
  shnu_mbcr_name4: str    #매수2 회원사 명4
  shnu_mbcr_name5: str    #매수2 회원사 명5
  total_shnu_qty1: str    #총 매수2 수량1
  total_shnu_qty2: str    #총 매수2 수량2
  total_shnu_qty3: str    #총 매수2 수량3
  total_shnu_qty4: str    #총 매수2 수량4
  total_shnu_qty5: str    #총 매수2 수량5
  shnu_mbcr_rlim1: str    #매수2 회원사 비중1
  shnu_mbcr_rlim2: str    #매수2 회원사 비중2
  shnu_mbcr_rlim3: str    #매수2 회원사 비중3
  shnu_mbcr_rlim4: str    #매수2 회원사 비중4
  shnu_mbcr_rlim5: str    #매수2 회원사 비중5
  shnu_qty_icdc1: str    #매수2 수량 증감1
  shnu_qty_icdc2: str    #매수2 수량 증감2
  shnu_qty_icdc3: str    #매수2 수량 증감3
  shnu_qty_icdc4: str    #매수2 수량 증감4
  shnu_qty_icdc5: str    #매수2 수량 증감5
  glob_total_seln_qty: str    #외국계 총 매도 수량
  glob_seln_rlim: str    #외국계 매도 비중
  glob_ntby_qty: str    #외국계 순매수 수량
  glob_total_shnu_qty: str    #외국계 총 매수2 수량
  glob_shnu_rlim: str    #외국계 매수2 비중
  seln_mbcr_glob_yn_1: str    #매도 회원사 외국계 여부1
  seln_mbcr_glob_yn_2: str    #매도 회원사 외국계 여부2
  seln_mbcr_glob_yn_3: str    #매도 회원사 외국계 여부3
  seln_mbcr_glob_yn_4: str    #매도 회원사 외국계 여부4
  seln_mbcr_glob_yn_5: str    #매도 회원사 외국계 여부5
  shnu_mbcr_glob_yn_1: str    #매수2 회원사 외국계 여부1
  shnu_mbcr_glob_yn_2: str    #매수2 회원사 외국계 여부2
  shnu_mbcr_glob_yn_3: str    #매수2 회원사 외국계 여부3
  shnu_mbcr_glob_yn_4: str    #매수2 회원사 외국계 여부4
  shnu_mbcr_glob_yn_5: str    #매수2 회원사 외국계 여부5
  glob_total_seln_qty_icdc: str    #외국계 총 매도 수량 증감
  glob_total_shnu_qty_icdc: str    #외국계 총 매수2 수량 증감

from dataclasses import dataclass

@dataclass
class KrStockDailyItemchartprice:
  prdy_vrss: str    # 전일 대비
  prdy_vrss_sign: str    # 전일 대비 부호
  prdy_ctrt: str    # 전일 대비율
  stck_prdy_clpr: str    # 주식 전일 종가
  acml_vol: str    # 누적 거래량
  acml_tr_pbmn: str    # 누적 거래 대금
  hts_kor_isnm: str    # HTS 한글 종목명
  stck_prpr: str    # 주식 현재가
  stck_shrn_iscd: str    # 주식 단축 종목코드
  prdy_vol: str    # 전일 거래량
  stck_mxpr: str    # 주식 상한가
  stck_llam: str    # 주식 하한가
  stck_oprc: str    # 주식 시가
  stck_hgpr: str    # 주식 최고가
  stck_lwpr: str    # 주식 최저가
  stck_prdy_oprc: str    # 주식 전일 시가
  stck_prdy_hgpr: str    # 주식 전일 최고가
  stck_prdy_lwpr: str    # 주식 전일 최저가
  askp: str    # 매도호가
  bidp: str    # 매수호가
  prdy_vrss_vol: str    # 전일 대비 거래량
  vol_tnrt: str    # 거래량 회전율
  stck_fcam: str    # 주식 액면가
  lstn_stcn: str    # 상장 주수
  cpfn: str    # 자본금
  hts_avls: str    # HTS 시가총액
  per: str    # PER
  eps: str    # EPS
  pbr: str    # PBR
  itewhol_loan_rmnd_ratem: str    # 전체 융자 잔고 비율

  stck_bsop_date: str    # 주식 영업 일자
  stck_clpr: str    # 주식 종가
  flng_cls_code: str    # 락 구분 코드
  prtt_rate: str    # 분할 비율
  mod_yn: str    # 변경 여부
  revl_issu_reas: str    # 재평가사유코드