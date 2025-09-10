# transformer/interfaces.py
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional

class DataFrameBuilder(ABC):
  """DataFrame 생성을 위한 빌더 인터페이스"""
  @abstractmethod
  def build(self, ticker: str, group: pd.DataFrame) -> Optional[pd.DataFrame]:
    pass

class TransformerStrategy(ABC):
  """데이터 변환 전략에 대한 인터페이스"""
  @abstractmethod
  def transform(self, raw_df: pd.DataFrame) -> pd.DataFrame:
    pass