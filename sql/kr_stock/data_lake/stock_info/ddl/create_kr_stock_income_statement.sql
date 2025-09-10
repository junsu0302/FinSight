-- KIS(한국투자증권) API의 "[국내주식] 종목정보 > 국내주식 손익계산서"의 데이터를 수집 
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_income_statement (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  stac_yymm TEXT NOT NULL,
  sale_account TEXT,
  sale_cost TEXT, 
  sale_totl_prfi TEXT,
  depr_cost TEXT,
  sell_mang TEXT,
  bsop_prti TEXT,
  bsop_non_ernn TEXT,
  bsop_non_expn TEXT,
  op_prfi TEXT,
  spec_prfi TEXT,
  spec_loss TEXT,
  thtr_ntin TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- ticker와 stac_yymm을 조합하여 고유성을 보장
  UNIQUE (ticker, stac_yymm)
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_income_statement IS '국내 주식 손익계산서 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_income_statement.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_income_statement.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_income_statement.stac_yymm IS '결산 년월';
COMMENT ON COLUMN kr_stock_income_statement.sale_account IS '매출액';
COMMENT ON COLUMN kr_stock_income_statement.sale_cost IS '매출 원가';
COMMENT ON COLUMN kr_stock_income_statement.sale_totl_prfi IS '매출 총 이익';
COMMENT ON COLUMN kr_stock_income_statement.depr_cost IS '감가상각비';
COMMENT ON COLUMN kr_stock_income_statement.sell_mang IS '판매 및 관리비';
COMMENT ON COLUMN kr_stock_income_statement.bsop_prti IS '영업 이익';
COMMENT ON COLUMN kr_stock_income_statement.bsop_non_ernn IS '영업 외 수익';
COMMENT ON COLUMN kr_stock_income_statement.bsop_non_expn IS '영업 외 비용';
COMMENT ON COLUMN kr_stock_income_statement.op_prfi IS '경상 이익';
COMMENT ON COLUMN kr_stock_income_statement.spec_prfi IS '특별 이익';
COMMENT ON COLUMN kr_stock_income_statement.spec_loss IS '특별 손실';
COMMENT ON COLUMN kr_stock_income_statement.thtr_ntin IS '당기순이익';
