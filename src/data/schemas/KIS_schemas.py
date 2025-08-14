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