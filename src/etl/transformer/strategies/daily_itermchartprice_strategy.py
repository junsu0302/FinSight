# transformer/strategies/daily_itemchart_strategy.py
import pandas as pd
from typing import Optional
from dataclasses import fields
from src.data.schemas.KIS_schemas import KrStockDailyItemchartprice  # 스키마 위치는 실제 프로젝트에 맞게 조정해주세요.
from ..interfaces import TransformerStrategy, DataFrameBuilder

class DailyItemchartPriceBuilder(DataFrameBuilder):
  """
  '주식일봉차트' 데이터 변환을 위한 구체적인 빌더 클래스.

  이 클래스는 한 종목(ticker)에 해당하는 원본 데이터를 받아,
  output1(기준 정보)과 output2(일자별 시세)를 결합하여 구조화된
  Pandas DataFrame 한 조각을 생성하는 책임을 가집니다.
  """
  def build(self, ticker: str, group: pd.DataFrame) -> Optional[pd.DataFrame]:
    """한 종목의 그룹화된 데이터를 받아 정제된 DataFrame을 생성합니다.

    Args:
      ticker (str): 현재 처리 중인 종목의 티커.
      group (pd.DataFrame): 해당 티커에 대한 모든 API 응답 행(output1, output2)을 포함하는 DataFrame.

    Returns:
      Optional[pd.DataFrame]: 성공적으로 변환된 경우, 해당 종목의 정제된
                              DataFrame을 반환합니다. 필수 데이터가 없으면 None을 반환합니다.
    """
    # [1] 데이터 분리: 처리를 용이하게 하기 위해 data_source를 기준으로
    #     output1(기준 정보)과 output2(일별 시세) DataFrame으로 분리합니다.
    output1_df = group[group['data_source'] == 'output1']
    output2_df = group[group['data_source'] == 'output2'].copy() # SettingWithCopyWarning 방지

    # [2] 필수 데이터 검증: 두 데이터 소스가 모두 존재하는지 확인합니다.
    if output1_df.empty or output2_df.empty:
      return None

    # [3] 기준 정보 추출 (from output1):
    # output1은 모든 날짜에 동일하게 적용될 메타데이터입니다.
    # 단, 일별 시세(output2)에 이미 존재하는 컬럼('stck_oprc' 등)은 제외하여
    # output2의 데이터가 우선권을 갖도록 합니다.
    output1_cols_to_use = [col for col in output1_df.columns if col not in output2_df.columns]
    output1_data = output1_df.iloc[0][output1_cols_to_use].to_dict()

    # [4] 데이터 결합:
    # 일별 시세 데이터(output2)의 모든 행에 [3]에서 추출한 기준 정보를 추가합니다.
    # 이로써 시계열 데이터프레임이 완성됩니다.
    combined_df = output2_df.assign(**output1_data)
    
    # [5] 공통 메타데이터 추가: 어떤 종목의 데이터인지 식별할 수 있도록 ticker를 추가합니다.
    combined_df['ticker'] = ticker
    
    return combined_df

class DailyItemchartPriceStrategy(TransformerStrategy):
  """
  '주식일봉차트' 데이터 변환을 위한 구체적인 전략 클래스.

  Builder를 사용하여 실제 변환 작업을 조율하는 Director의 역할을 수행합니다.
  """
  def __init__(self):
    """DailyItemchartPriceStrategy의 인스턴스를 초기화합니다."""
    self._builder = DailyItemchartPriceBuilder()
  
  def transform(self, raw_df: pd.DataFrame) -> pd.DataFrame:
    """'주식일봉차트' 원본 DataFrame을 DB 스키마에 맞는 최종 형태로 변환합니다.

    Args:
      raw_df (pd.DataFrame): 여러 종목의 API 응답이 혼합된 원본 DataFrame.

    Returns:
      pd.DataFrame: 최종적으로 정제되고 DB 스키마에 맞춰 컬럼이 정렬된 DataFrame.
    """
    if raw_df.empty:
      return pd.DataFrame()

    processed_records = []

    # [1] 전체 종목에 대한 빌드 작업 지시(Direct):
    #     Builder에게 종목별 데이터 조각 생성을 위임합니다.
    for ticker, group in raw_df.groupby('ticker'):
      built_df = self._builder.build(ticker, group)
      if built_df is not None:
        processed_records.append(built_df)

    if not processed_records:
      return pd.DataFrame()
        
    # [2] 결과 취합 및 최종 DataFrame 생성:
    #     Builder가 생성한 모든 종목의 DataFrame 조각들을 하나로 합칩니다.
    final_df = pd.concat(processed_records, ignore_index=True)
    
    # [3] 최종 스키마 정렬:
    #     요청하신 dataclass(KrStockDailyItemchartPriceprice) 스키마와 완전히 일치하도록
    #     컬럼 순서를 조정하고, 누락된 컬럼은 None으로 채웁니다.
    schema_columns = [field.name for field in fields(KrStockDailyItemchartprice)]
    
    # 참고: DB 저장을 위해 'ticker' 컬럼도 최종 스키마에 포함하는 것을 권장합니다.
    # 필요하다면 아래와 같이 처리할 수 있습니다.
    if 'ticker' not in schema_columns:
      schema_columns.insert(0, 'ticker')

    for col in schema_columns:
      if col not in final_df.columns:
        final_df[col] = None
            
    return final_df[schema_columns]