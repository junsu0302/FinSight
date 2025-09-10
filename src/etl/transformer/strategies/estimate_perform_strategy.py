# transformer/strategies/estimate_perform_strategy.py
import pandas as pd
from typing import Optional
from dataclasses import fields
from src.data.schemas.KIS_schemas import KrStockEstimatePerform
from ..interfaces import TransformerStrategy, DataFrameBuilder

class EstimatePerformBuilder(DataFrameBuilder):
  """'종목추정실적' 데이터 변환을 위한 구체적인 빌더 클래스.

  이 클래스는 한 종목(ticker)에 해당하는 원본 데이터를 받아,
  구조화된 Pandas DataFrame 한 조각을 생성하는 책임을 가집니다.
  복잡한 DataFrame 생성 과정을 캡슐화합니다.
  """
  def build(self, ticker: str, group: pd.DataFrame) -> Optional[pd.DataFrame]:
    """한 종목의 그룹화된 데이터를 받아 정제된 DataFrame을 생성합니다.

    Args:
      ticker (str): 현재 처리 중인 종목의 티커.
      group (pd.DataFrame): 해당 티커에 대한 모든 API 응답 행을 포함하는 DataFrame.

    Returns:
      Optional[pd.DataFrame]: 성공적으로 변환된 경우, 해당 종목의 정제된
                              DataFrame을 반환합니다. 필수 데이터가 없거나
                              형식이 맞지 않으면 None을 반환합니다.
    """
    # ----- 내 스타일 주석 -----
    # [1] API 응답 재구성: 처리를 용이하게 하기 위해 DataFrame 그룹을 다시
    #     딕셔너리 리스트로 변환하고, 각 output 블록별로 데이터를 분리합니다.
    api_response_list = group.to_dict('records')
    
    output1 = next((d for d in api_response_list if d.get('data_source') == 'output1'), {})
    output2 = [d for d in api_response_list if d.get('data_source') == 'output2']
    output3 = [d for d in api_response_list if d.get('data_source') == 'output3']
    output4 = [d for d in api_response_list if d.get('data_source') == 'output4']
    
    # [2] 필수 데이터 검증: 변환에 필요한 모든 output 블록이 존재하는지 확인합니다.
    if not all([output1, output2, output3, output4]):
      return None

    # [3] DataFrame 구조 정의:
    # output4에서 기간 정보를 추출하여 최종 DataFrame의 컬럼명으로 사용합니다.
    columns = [item['dt'] for item in output4]
    
    # KIS API 응답 순서와 정확히 일치해야 하는 행(index) 이름을 명시적으로 선언합니다.
    index_names = [
      'revenue', 'revenue_yoy', 'operating_profit', 'operating_profit_yoy', 
      'net_income', 'net_income_yoy', 'eps', 'per', 'bps', 'pbr', 
      'roe', 'ev_ebitda', 'sps', 'psr' 
    ]
    
    # [4] 데이터 정합성 검증: API로부터 받은 데이터 행의 개수와 우리가 정의한
    #     행 이름의 개수가 일치하는지 확인합니다.
    data_rows = output2 + output3
    if len(data_rows) != len(index_names):
      return None

    # [5] DataFrame 생성 및 가공:
    # 먼저 데이터 부분만으로 DataFrame을 만들고, 실제 기간 개수만큼 컬럼을 선택합니다.
    df = pd.DataFrame(data_rows, columns=[f'data{i+1}' for i in range(5)])
    df = df.iloc[:, :len(columns)]
    # 위에서 정의한 컬럼명과 인덱스명을 DataFrame에 적용합니다.
    df.columns = columns
    df.index = index_names
    
    # [6] 최종 형태 변환: 모든 재무 데이터를 숫자(float) 타입으로 변환하고,
    #     분석이 용이하도록 행과 열을 전환(Transpose)합니다.
    df = df.astype(float).transpose()
    
    # [7] 공통 메타데이터 추가: output1에 있던 티커, 애널리스트, 투자의견 등
    #     공통 정보를 모든 행에 추가합니다.
    df['ticker'] = ticker
    df['analyst'] = output1.get('name1')
    df['opinion'] = output1.get('rcmd_name')
    
    return df

class EstimatePerformStrategy(TransformerStrategy):
  """'종목추정실적' 데이터 변환을 위한 구체적인 전략 클래스.

  이 클래스는 Builder를 사용하여 실제 변환 작업을 조율하는 Director의
  역할을 수행합니다. 여러 종목의 데이터를 반복 처리하고 최종 결과물을
  DB 스키마에 맞게 정리하는 책임을 가집니다.
  """
  def __init__(self):
    """EstimatePerformStrategy의 인스턴스를 초기화합니다."""
    self._builder = EstimatePerformBuilder()
  
  def transform(self, raw_df: pd.DataFrame) -> pd.DataFrame:
    """'종목추정실적' 원본 DataFrame을 DB 스키마에 맞는 최종 형태로 변환합니다.

    Args:
      raw_df (pd.DataFrame): 여러 종목의 API 응답이 혼합된 원본 DataFrame.

    Returns:
      pd.DataFrame: 최종적으로 정제되고 DB 스키마에 맞춰 컬럼이 정렬된
                    DataFrame을 반환합니다.
    """
    if raw_df.empty:
      return pd.DataFrame()

    processed_records = []

    # [1] 전체 종목에 대한 빌드 작업 지시(Direct):
    #     원본 DataFrame을 종목(ticker)별로 그룹화한 뒤, 각 그룹을 Builder에게
    #     전달하여 개별 DataFrame 조각을 생성하도록 지시합니다.
    for ticker, group in raw_df.groupby('ticker'):
      built_df = self._builder.build(ticker, group)
      if built_df is not None:
        processed_records.append(built_df)

    if not processed_records:
      return pd.DataFrame()
        
    # [2] 결과 취합 및 최종 DataFrame 생성:
    #     Builder가 생성한 모든 종목의 DataFrame 조각들을 하나로 합칩니다.
    #     기존 인덱스(기간 정보)는 'period'라는 새로운 컬럼으로 변경합니다.
    final_df = pd.concat(processed_records).reset_index().rename(columns={'index': 'period'})
    
    # [3] 최종 스키마 정렬:
    #     dataclass(KrStockEstimatePerform)로부터 최종 DB 테이블의 컬럼 순서를 가져옵니다.
    #     누락된 컬럼이 있다면 None으로 채우고, 최종적으로 스키마와 동일한 순서로
    #     컬럼을 정렬하여 반환합니다. 이는 DB 적재 시 오류를 방지합니다.
    schema_columns = [field.name for field in fields(KrStockEstimatePerform)]
    for col in schema_columns:
      if col not in final_df.columns:
        final_df[col] = None
            
    return final_df[schema_columns]