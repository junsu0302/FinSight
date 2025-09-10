# src/utils/debug_utils.py
import pandas as pd
from dataclasses import fields

def inspect_dataframe_schema(df: pd.DataFrame, schema_class: type, stage: str = "N/A"):
  """
  DataFrame의 상태와 스키마를 비교하여 상세한 디버깅 리포트를 출력합니다.

  Args:
      df (pd.DataFrame): 검사할 DataFrame.
      schema_class (type): 비교 기준으로 사용할 dataclass.
      stage (str): 리포트에 표시될 현재 검사 단계를 설명하는 문자열.
  """
  print("\n" + "="*20 + f" [ FinSight DataFrame Inspector: {stage} ] " + "="*20)
  
  if df.empty:
    print("⚠️ DataFrame이 비어있습니다.")
    print("="*80 + "\n")
    return

  # 스키마 정보
  schema_columns = {field.name for field in fields(schema_class)}
  print(f"✅ 스키마 '{schema_class.__name__}' 기준 컬럼 수: {len(schema_columns)}개")

  # DataFrame 정보
  df_columns = set(df.columns)
  print(f"✅ 현재 DataFrame의 컬럼 수: {len(df_columns)}개")

  # 비교 분석
  missing_in_df = schema_columns - df_columns
  if missing_in_df:
    print(f"   - ⚠️ 스키마에 있으나 DataFrame에 없는 컬럼: {sorted(list(missing_in_df))}")

  extra_in_df = df_columns - schema_columns
  if extra_in_df:
    print(f"   - 💡 DataFrame에만 존재하는 추가 컬럼: {sorted(list(extra_in_df))}")
      
  if not missing_in_df and not extra_in_df:
    print("   - ✨ 모든 컬럼이 스키마와 정확히 일치합니다.")

  print("="*80 + "\n")