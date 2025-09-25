# preprocessor.py 수정 후 최종 코드

import pandas as pd
from tasks import Task

class DataFramePreprocessor:
  def __init__(self, df: pd.DataFrame, verbose: bool = False):
    """
    Args:
      df (pd.DataFrame): 처리할 데이터프레임
      verbose (bool): True이면 파이프라인 실행 로그를 출력
    """
    self.df = df.copy()
    self.tasks = []
    self.verbose = verbose

  def add_task(self, task: Task):
    self.tasks.append(task)
    return self

  def process(self) -> pd.DataFrame:
    for task in self.tasks:
      self.df = task.execute(self.df, verbose=self.verbose) 
      
    return self.df