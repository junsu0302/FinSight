# src/tasks.py
import warnings
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

class Task(ABC):
  """모든 전처리 작업의 기본이 되는 추상 클래스"""
  @abstractmethod
  def execute(self, df: pd.DataFrame) -> pd.DataFrame:
    pass

class MissingValueCleaner(Task):
  """빈 문자열과 설정된 값들을 결측값(NaN)으로 변환하는 작업"""
  def __init__(self, values_to_replace=None):
    self.values_to_replace = values_to_replace if values_to_replace else [['0', 0]]

  def execute(self, df: pd.DataFrame, verbose: bool) -> pd.DataFrame:
    with warnings.catch_warnings():
      warnings.simplefilter("ignore", FutureWarning)
      
      for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].replace(r'^\s*$', np.nan, regex=True).infer_objects(copy=False)
        for val in self.values_to_replace:
          df[col] = df[col].replace(val, np.nan).infer_objects(copy=False)
          
    return df

class NullColumnRemover(Task):
  """결측치 개수가 기준치를 넘는 컬럼을 제거하는 작업"""
  def __init__(self, threshold_count: int = 100):
    self.threshold = threshold_count

  def execute(self, df: pd.DataFrame, verbose: bool) -> pd.DataFrame:
    missing_counts = df.isnull().sum()
    cols_to_drop = missing_counts[missing_counts >= self.threshold].index
    if not cols_to_drop.empty:
      if verbose:
        print(f"NullColumnRemover {len(cols_to_drop)} columns (threshold >= {self.threshold}) : {cols_to_drop.tolist()}")
    return df.drop(columns=cols_to_drop)

class ConstantColumnRemover(Task):
  """고유값이 기준치 이하인 상수 컬럼을 제거하는 작업"""
  def __init__(self, nunique_threshold: int = 1):
    self.threshold = nunique_threshold

  def execute(self, df: pd.DataFrame, verbose: bool) -> pd.DataFrame:
    nunique = df.nunique()
    cols_to_drop = nunique[nunique <= self.threshold].index
    if not cols_to_drop.empty:
      if verbose:
        print(f"ConstantColumnRemover {len(cols_to_drop)} columns (nunique <= {self.threshold}) : {cols_to_drop.tolist()}")
    return df.drop(columns=cols_to_drop)

class ColumnSelector(Task):
  """분석가가 수동으로 선택한 컬럼만 남기는 작업"""
  def __init__(self, columns_to_keep: list):
    self.columns_to_keep = columns_to_keep

  def execute(self, df: pd.DataFrame, verbose: bool) -> pd.DataFrame:
    valid_cols = [col for col in self.columns_to_keep if col in df.columns]

    if verbose:
      print(f"ColumnSelector: {len(df.columns) - len(valid_cols)} columns : {self.columns_to_keep}")

    return df[valid_cols]

class AutomaticTypeConverter(Task):
  """저비율 카테고리 및 날짜 타입을 자동으로 변환하는 작업"""
  def __init__(self, category_ratio: float = 0.05, date_success_rate: float = 0.95):
    self.category_ratio = category_ratio
    self.date_success_rate = date_success_rate

  def execute(self, df: pd.DataFrame, verbose: bool) -> pd.DataFrame:
    object_cols = df.select_dtypes(include='object').columns.copy() # 복사본 사용
    for col in object_cols:
      # 날짜 변환
      valid_count = df[col].count()
      is_date_converted = False
      
      if valid_count > 0:
        for fmt in [None, '%Y%m%d', '%Y-%m-%d', '%Y%m', '%Y-%m']:
          with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            date_series = pd.to_datetime(df[col], format=fmt, errors='coerce')
            
          if date_series.count() / valid_count > self.date_success_rate:
            df[col] = date_series
            is_date_converted = True
            break
      
      if is_date_converted:
        continue

      # 카테고리 변환
      if df[col].nunique() == 0:
        continue
      if df[col].nunique() / len(df[col]) < self.category_ratio:
        df[col] = df[col].astype('category')

    return df

class ManualTypeConverter(Task):
  """분석가가 직접 정의한 맵을 기준으로 타입을 변환하는 작업"""
  def __init__(self, dtype_map: dict):
    self.dtype_map = dtype_map

  def execute(self, df: pd.DataFrame, verbose: bool) -> pd.DataFrame:
    if verbose:
      print("Executing: ManualTypeConverter")

    # 데이터 타입(dtype)을 기준으로 반복
    for dtype, cols in self.dtype_map.items():
      # DataFrame에 실제 존재하는 컬럼만 필터링
      valid_cols = [col for col in cols if col in df.columns]
      if not valid_cols:
        continue

      try:
        # 숫자 타입 (int, float) 공통 전처리
        # dtype 문자열을 소문자로 변환하여 'int' 또는 'float' 포함 여부 확인
        if 'int' in dtype.lower() or 'float' in dtype.lower():
          # 여러 컬럼에 대해 쉼표(,) 제거를 한 번에 수행
          for col in valid_cols:
            if df[col].dtype == 'object':
              df[col] = df[col].str.replace(',', '', regex=False)
          
          # 실제 타입 변환
          if 'int' in dtype.lower():
            # NaN을 지원하는 Int64로 안전하게 변환
            df[valid_cols] = df[valid_cols].apply(pd.to_numeric, errors='coerce')
            for col in valid_cols: # .astype('Int64')는 Series 단위로 적용
              if not df[col].isnull().all():
                df[col] = df[col].astype('Int64')
          else: # float
            df[valid_cols] = df[valid_cols].apply(pd.to_numeric, errors='coerce')

        # 날짜 타입
        elif 'datetime' in dtype.lower():
          for col in valid_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        # 그 외 타입 (e.g., category, object, bool)
        else:
          df[valid_cols] = df[valid_cols].astype(dtype)

      except (ValueError, TypeError) as e:
        if verbose:
          print(f" -> Warning: Could not convert columns {valid_cols} to '{dtype}'. Error: {e}")
          
    return df