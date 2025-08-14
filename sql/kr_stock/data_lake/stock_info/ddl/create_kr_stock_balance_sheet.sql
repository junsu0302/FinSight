-- KIS(한국투자증권) API의 "[국내주식] 종목정보 > 국내주식 대차대조표"의 데이터를 수집 
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_balance_sheet(
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  stac_yymm TEXT NOT NULL,
  cras TEXT,
  fxas TEXT,
  total_aset TEXT,
  flow_lblt TEXT,
  fix_lblt TEXT,
  total_lblt TEXT,
  cpfn TEXT,
  cfp_surp TEXT,
  prfi_surp TEXT,
  total_cptl TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- ticker와 stac_yymm을 조합하여 고유성을 보장
  UNIQUE (ticker, stac_yymm)
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_balance_sheet IS '국내 주식 대차대조표 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_balance_sheet.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_balance_sheet.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_balance_sheet.stac_yymm IS '결산 년월';
COMMENT ON COLUMN kr_stock_balance_sheet.cras IS '유동자산';
COMMENT ON COLUMN kr_stock_balance_sheet.fxas IS '고정자산';
COMMENT ON COLUMN kr_stock_balance_sheet.total_aset IS '자산총계';
COMMENT ON COLUMN kr_stock_balance_sheet.flow_lblt IS '유동부채';
COMMENT ON COLUMN kr_stock_balance_sheet.fix_lblt IS '고정부채';
COMMENT ON COLUMN kr_stock_balance_sheet.total_lblt IS '부채총계';
COMMENT ON COLUMN kr_stock_balance_sheet.cpfn IS '자본금';
COMMENT ON COLUMN kr_stock_balance_sheet.cfp_surp IS '자본 잉여금';
COMMENT ON COLUMN kr_stock_balance_sheet.prfi_surp IS '이익 잉여금';
COMMENT ON COLUMN kr_stock_balance_sheet.total_cptl IS '자본총계';
COMMENT ON COLUMN kr_stock_balance_sheet.updated_at IS '데이터 마지막 수집 시간';