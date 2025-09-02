# transformer/strategies/asking_price_strategy.py
import pandas as pd
from typing import Optional
from dataclasses import fields
from src.data.schemas.KIS_schemas import KrStockAskingPrice
from ..interfaces import TransformerStrategy, DataFrameBuilder

class AskingPriceBuilder(DataFrameBuilder):
  """
  '주식호가' 데이터 변환을 위한 구체적인 빌더 클래스.

  이 클래스는 한 종목(ticker)에 해당하는 output1과 output2 데이터를 받아,
  하나의 정제된 데이터 행(row)을 생성하는 책임을 가집니다.
  """
  def build(self, ticker: str, group: pd.DataFrame) -> Optional[pd.DataFrame]:
    """한 종목의 그룹화된 데이터를 받아 정제된 DataFrame을 생성합니다.

    Args:
      ticker (str): 현재 처리 중인 종목의 티커.
      group (pd.DataFrame): 해당 티커에 대한 모든 API 응답 행을 포함하는 DataFrame.

    Returns:
      Optional[pd.DataFrame]: 성공적으로 변환된 경우, 해당 종목의 정제된
                              DataFrame(단일 행)을 반환합니다. 필수 데이터가 없으면 None을 반환합니다.
    """
    # [1] 데이터 분리: data_source를 기준으로 output1과 output2로 분리합니다.
    output1_df = group[group['data_source'] == 'output1'].reset_index(drop=True)
    output2_df = group[group['data_source'] == 'output2'].reset_index(drop=True)

    # [2] 필수 데이터 검증: 두 데이터 소스가 모두 존재하는지 확인합니다.
    if output1_df.empty or output2_df.empty:
      return None

    # [3] 데이터 결합: output1과 output2는 동일 시점의 데이터이므로, 컬럼(column) 기준으로 결합합니다.
    output1_series = output1_df.iloc[0]
    output2_series = output2_df.iloc[0]
    
    # [4] 중복 컬럼 제거:
    # output1의 컬럼을 기준으로, output2에 중복된 컬럼이 있다면 제거합니다.
    # 이를 통해 데이터 병합 시 발생할 수 있는 'duplicate labels' 오류를 방지합니다.
    output2_unique_series = output2_series.drop(
        labels=output1_series.index, 
        errors='ignore' # output2에 output1 컬럼이 없는 경우 오류를 무시합니다.
    )
    
    # 중복이 제거된 Series들을 안전하게 병합합니다.
    combined_series = pd.concat([output1_series, output2_unique_series])
    
    # [5] DataFrame 생성 및 메타데이터 추가:
    # 생성된 Series를 단일 행을 가진 DataFrame으로 변환하고 ticker 정보를 추가합니다.
    combined_df = combined_series.to_frame().T
    combined_df['ticker'] = ticker

    # [6] 불필요 컬럼 제거
    if 'data_source' in combined_df.columns:
      combined_df = combined_df.drop(columns=['data_source'])
    
    return combined_df

class AskingPriceStrategy(TransformerStrategy):
  """
  '주식호가' 데이터 변환을 위한 구체적인 전략 클래스.
  Builder를 사용하여 실제 변환 작업을 조율하는 Director의 역할을 수행합니다.
  """
  def __init__(self):
    """AskingPriceStrategy의 인스턴스를 초기화합니다."""
    self._builder = AskingPriceBuilder()
    self._schema_columns = [field.name for field in fields(KrStockAskingPrice)]
  
  def transform(self, raw_df: pd.DataFrame) -> pd.DataFrame:
    """'주식호가' 원본 DataFrame을 DB 스키마에 맞는 최종 형태로 변환합니다."""
    if raw_df.empty:
      return pd.DataFrame()

    processed_records = []

    for ticker, group in raw_df.groupby('ticker'):
      built_df = self._builder.build(ticker, group)
      if built_df is not None:
        processed_records.append(built_df)

    if not processed_records:
      return pd.DataFrame()
        
    final_df = pd.concat(processed_records, ignore_index=True)
    
    for col in self._schema_columns:
      if col not in final_df.columns:
        final_df[col] = None

    return final_df[self._schema_columns]