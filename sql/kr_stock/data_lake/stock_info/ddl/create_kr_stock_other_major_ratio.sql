-- KIS(한국투자증권) API의 "[국내주식] 종목정보 > 국내주식 기타주요비율"의 데이터를 수집 
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_other_major_ratio (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  stac_yymm TEXT NOT NULL,
  payout_rate TEXT,
  eva TEXT,
  ebitda TEXT,
  ev_ebitda TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- ticker와 stac_yymm을 조합하여 고유성을 보장
  UNIQUE (ticker, stac_yymm)
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_other_major_ratio IS '국내 주식 기타 주요비율 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_other_major_ratio.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_other_major_ratio.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_other_major_ratio.stac_yymm IS '결산 년월';
COMMENT ON COLUMN kr_stock_other_major_ratio.payout_rate IS '배당 성향';
COMMENT ON COLUMN kr_stock_other_major_ratio.eva IS 'EVA';
COMMENT ON COLUMN kr_stock_other_major_ratio.ebitda IS 'EBITDA';
COMMENT ON COLUMN kr_stock_other_major_ratio.ev_ebitda IS 'EV/EBITDA';
COMMENT ON COLUMN kr_stock_other_major_ratio.updated_at IS '데이터 마지막 수집 시간';