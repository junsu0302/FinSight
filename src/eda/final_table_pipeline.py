import pandas as pd
import numpy as np
from src.data.db_handler import DBHandler # 사용자 환경에 맞게 경로 수정 필요

def create_merged_master_table():
    """
    Daily, Quartely, Static 데이터를 병합하여 최종 마스터 테이블을 생성합니다.
    (merge_asof를 사용하지 않는 새로운 방식)
    """
    db_handler = DBHandler(db_name="data_warehouse")

    # 1. 세 개의 테이블을 데이터베이스에서 로드
    print("--- 1. 데이터 로드 시작 ---")
    df_daily = db_handler.fetch_data("kr_stock_daily_itemchartprice")
    print(f"Loaded kr_stock_daily_data: {df_daily.shape}")

    df_quartely = db_handler.fetch_data("kr_stock_quartely_data")
    print(f"Loaded kr_stock_quartely_data: {df_quartely.shape}")

    df_static = db_handler.fetch_data("kr_stock_static_data")
    print(f"Loaded kr_stock_static_data: {df_static.shape}")

    # 2. Daily-Quartely 병합 (NumPy를 이용한 수동 매핑)
    print("\n--- 2. Daily 데이터에 Quartely 데이터 결합 시작 (신규 방식) ---")

    # 전처리
    for df in [df_daily, df_quartely, df_static]:
        df.dropna(subset=['ticker'], inplace=True)
        df['ticker'] = df['ticker'].astype(str)

    df_daily['stck_bsop_date'] = pd.to_datetime(df_daily['stck_bsop_date'], errors='coerce')
    df_quartely['stac_yymm'] = pd.to_datetime(df_quartely['stac_yymm'], errors='coerce')
    df_daily.dropna(subset=['stck_bsop_date'], inplace=True)
    df_quartely.dropna(subset=['stac_yymm'], inplace=True)

    df_daily = df_daily.sort_values(by=['ticker', 'stck_bsop_date']).reset_index(drop=True)
    df_quartely = df_quartely.sort_values(by=['ticker', 'stac_yymm']).reset_index(drop=True)

    # 각 daily 날짜가 어느 quartely 날짜 구간에 속하는지 인덱스를 계산
    daily_dates = df_daily['stck_bsop_date']
    quartely_dates = df_quartely['stac_yymm']
    
    daily_idx = df_daily.groupby('ticker').stck_bsop_date.count().cumsum()
    quartely_idx = df_quartely.groupby('ticker').stac_yymm.count().cumsum()
    
    quartely_indices = np.full(len(df_daily), -1, dtype=np.int64)

    last_d_idx = 0
    last_q_idx = 0
    for ticker in df_daily['ticker'].unique():
        d_idx = daily_idx.get(ticker, last_d_idx)
        q_idx = quartely_idx.get(ticker, last_q_idx)
        
        d_dates_group = daily_dates.iloc[last_d_idx:d_idx]
        q_dates_group = quartely_dates.iloc[last_q_idx:q_idx]

        if not q_dates_group.empty:
            indices = q_dates_group.searchsorted(d_dates_group, side='right') - 1
            quartely_indices[last_d_idx:d_idx] = indices + last_q_idx

        last_d_idx = d_idx
        last_q_idx = q_idx

    # --- 🐞 최종 오류 해결 로직 ---
    # quartely_indices 배열에서 -1 값을 임시로 0으로 변경하여 KeyError를 방지합니다.
    safe_indices = quartely_indices.copy()
    invalid_mask = (safe_indices == -1)
    safe_indices[invalid_mask] = 0 # 임시로 0번 인덱스를 가리키게 함

    # 안전한 인덱스를 사용하여 데이터 조회
    quartely_cols = df_quartely.columns.drop(['ticker', 'stac_yymm'])
    new_values = df_quartely.loc[safe_indices, quartely_cols].values

    # 이전에 -1이었던 위치의 데이터들을 실제 결측치(NaN)로 덮어씁니다.
    new_values[invalid_mask] = np.nan
    
    # 최종적으로 값을 할당합니다.
    df_daily[quartely_cols] = new_values
    # ---------------------------------
    
    df_merged_daily_quartely = df_daily
    print(f"Daily + Quartely 결합 완료. 결과 Shape: {df_merged_daily_quartely.shape}")
    
    # 3. Static 데이터 병합 (일반 merge)
    print("\n--- 3. Static 데이터 결합 시작 ---")
    
    final_df = pd.merge(
        df_merged_daily_quartely,
        df_static,
        on='ticker',
        how='left'
    )
    print(f"Static 데이터 결합 완료. 최종 Shape: {final_df.shape}")

    # 4. 최종 결과 저장
    print("\n--- 4. 최종 결과 저장 ---")
    final_table_name = "stock_master_final"
    db_handler.replace_table_from_df(df=final_df, table_name=final_table_name)
    print(f"✅ 성공! 최종 마스터 테이블 '{final_table_name}'이(가) DB에 저장되었습니다.")

    return final_df

if __name__ == "__main__":
  master_table = create_merged_master_table()
  
  print("\n--- 최종 결과 샘플 ---")
  print(master_table.head())
  print("\n--- 최종 결과 정보 ---")
  master_table.info()