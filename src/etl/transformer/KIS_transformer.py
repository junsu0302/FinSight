# transformer/main_transformer.py
import pandas as pd
from typing import Dict

from .interfaces import TransformerStrategy
from .strategies.estimate_perform_strategy import EstimatePerformStrategy
from .strategies.asking_price_strategy import AskingPriceStrategy
from .strategies.daily_itermchartprice_strategy import DailyItemchartPriceStrategy

class KISTransformer:
  """
  KIS API 데이터 변환을 위한 메인 클래스(Context).
  모든 변환 전략을 관리하고 실행하는 단일 진입점 역할을 합니다.
  """
  def __init__(self):
    self._strategies: Dict[str, TransformerStrategy] = {
      "estimate_perform": EstimatePerformStrategy(),
      "asking_price": AskingPriceStrategy(),
      "daily_itemchartprice": DailyItemchartPriceStrategy(),
      }

  def transform(self, transformer_name: str, raw_df: pd.DataFrame) -> pd.DataFrame:
    strategy = self._strategies.get(transformer_name)
    if not strategy:
      raise ValueError(f"Unsupported transformer_name: '{transformer_name}'")
    
    return strategy.transform(raw_df)