import pandas as pd
from typing import List, Dict, Any
from src.data.schemas.KIS_schemas import KrStockEstimatePerform
from dataclasses import fields

class KISTransformer:
  """KIS API로부터 받은 원본 데이터를 분석 가능한 Pandas DataFrame으로 변환합니다."""

  def transform_estimate_perform(self, raw_df: pd.DataFrame) -> pd.DataFrame:
    """'종목추정실적' API의 원본 데이터프레임을 최종 분석용 DataFrame으로 변환합니다.

    이 함수는 여러 종목의 API 응답이 뒤섞여 있는 원본 DataFrame을 입력받아,
    종목별로 그룹화하고, 복잡한 구조를 피벗(pivot)하여 사람이 읽기 쉬운
    하나의 정제된 DataFrame으로 재구성합니다.

    Args:
      raw_df (pd.DataFrame): KIS_collector가 수집한 원본 데이터프레임.
                             'ticker'와 API 원본 응답 필드들을 포함합니다.

    Returns:
      pd.DataFrame: KrStockEstimatePerform 스키마에 맞춰 정제되고 컬럼이 정렬된
                    최종 데이터프레임.
    """
    # 입력된 DataFrame이 비어있으면, 빈 DataFrame을 즉시 반환
    if raw_df.empty:
      return pd.DataFrame()

    processed_records = []
    # DataFrame을 'ticker' 기준으로 그룹화하여 종목 단위로 하나씩 처리
    for ticker, group in raw_df.groupby('ticker'):
      # 그룹화된 데이터를 다시 딕셔너리의 리스트 형태로 변환 (처리 용이성)
      api_response_list = group.to_dict('records')
      
      # 'data_source' 키를 기준으로 output 블록별로 데이터 재구성
      output1 = next((d for d in api_response_list if d.get('data_source') == 'output1'), {})
      output2 = [d for d in api_response_list if d.get('data_source') == 'output2']
      output3 = [d for d in api_response_list if d.get('data_source') == 'output3']
      output4 = [d for d in api_response_list if d.get('data_source') == 'output4']
      
      # 필수적인 output 블록이 하나라도 없으면 해당 종목은 건너뜀
      if not all([output1, output2, output3, output4]):
        continue

      # output4에서 컬럼 이름(기간 정보) 추출 (예: '2022.12E')
      columns = [item['dt'] for item in output4]
      
      # API 문서 순서에 따라 행 이름(재무 항목)을 직접 정의
      index_names = [
          'revenue', 'revenue_yoy', 'operating_profit', 'operating_profit_yoy', 
          'net_income', 'net_income_yoy', 'eps', 'per', 'bps', 'pbr', 
          'roe', 'ev_ebitda', 'sps', 'psr' 
      ]
      
      # 데이터 부분(output2, output3)을 합치고, 행 개수가 맞는지 확인
      data_rows = output2 + output3
      if len(data_rows) != len(index_names): continue

      # 데이터로 DataFrame 생성 (컬럼은 임시 이름 부여)
      df = pd.DataFrame(data_rows, columns=[f'data{i+1}' for i in range(5)])
      df = df.iloc[:, :len(columns)] # 실제 기간 개수만큼 컬럼 선택
      
      # 컬럼과 인덱스에 올바른 이름 부여
      df.columns = columns
      df.index = index_names
      
      # 모든 데이터를 숫자(float) 타입으로 변환 후, 행과 열을 전환(Transpose)
      df = df.astype(float).transpose()
      
      # output1의 기본 정보를 모든 행에 추가
      df['ticker'] = ticker
      df['analyst'] = output1.get('name1')
      df['opinion'] = output1.get('rcmd_name')
      
      processed_records.append(df)

    if not processed_records:
      return pd.DataFrame()
        
    # 모든 종목에 대해 처리된 DataFrame들을 하나로 합침
    final_df = pd.concat(processed_records).reset_index().rename(columns={'index': 'period'})
    
    # 최종 DB 스키마에 맞춰 누락된 컬럼을 None으로 추가
    schema_columns = [field.name for field in fields(KrStockEstimatePerform)]
    for col in schema_columns:
        if col not in final_df.columns:
            final_df[col] = None
            
    return final_df