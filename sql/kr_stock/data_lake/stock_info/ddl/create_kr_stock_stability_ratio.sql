-- KIS(한국투자증권) API의 "[국내주식] 종목정보 > 국내주식 안정성비율"의 데이터를 수집 
-- 이 테이블은 API의 원본 데이터를 그대로 저장하는 Data Lake 역할 수행

CREATE TABLE IF NOT EXISTS kr_stock_stability_ratio (
  id SERIAL PRIMARY KEY,
  ticker TEXT NOT NULL,
  stac_yymm TEXT NOT NULL,
  lblt_rate TEXT,
  bram_depn TEXT,
  crnt_rate TEXT,
  quck_rate TEXT,

  -- 데이터 수집 시간을 기록
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

  -- ticker와 stac_yymm을 조합하여 고유성을 보장
  UNIQUE (ticker, stac_yymm)
);

-- 각 컬럼에 대한 설명(주석)을 추가
COMMENT ON TABLE kr_stock_stability_ratio IS '국내 주식 안정성비율 원본 데이터 테이블';
COMMENT ON COLUMN kr_stock_stability_ratio.id IS '행 고유 ID';
COMMENT ON COLUMN kr_stock_stability_ratio.ticker IS '데이터 조회의 기준이 된 종목코드';
COMMENT ON COLUMN kr_stock_stability_ratio.stac_yymm IS '결산 년월';
COMMENT ON COLUMN kr_stock_stability_ratio.lblt_rate IS '부채 비율';
COMMENT ON COLUMN kr_stock_stability_ratio.bram_depn IS '차입금 의존도';
COMMENT ON COLUMN kr_stock_stability_ratio.crnt_rate IS '유동 비율';
COMMENT ON COLUMN kr_stock_stability_ratio.quck_rate IS '당좌 비율';
COMMENT ON COLUMN kr_stock_stability_ratio.updated_at IS '데이터 마지막 수집 시간';