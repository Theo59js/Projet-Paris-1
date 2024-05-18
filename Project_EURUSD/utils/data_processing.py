import pandas as pd


def process_data(bloom_df):
    # Créer les différents dataframes et les traiter
    pass


def create_predict_dataframe(libor_data, ester_data):
    libor_dates = pd.to_datetime(libor_data['dates'], format='%d/%m/%Y')
    ester_dates = pd.to_datetime(ester_data['dates'], format='%d/%m/%Y')
    libor_df = pd.DataFrame({'date': libor_dates, 'liborusd_ov_predict': libor_data['values']})
    ester_df = pd.DataFrame({'date': ester_dates, 'estereonia_predict': ester_data['values']})
    combined_df = pd.merge(libor_df, ester_df, on='date', how='outer')
    combined_df.sort_values(by='date', inplace=True)
    combined_df['liborusd_ov_predict'] = combined_df['liborusd_ov_predict'].ffill()
    combined_df['estereonia_predict'] = combined_df['estereonia_predict'].ffill()
    combined_df = combined_df[['date', 'liborusd_ov_predict', 'estereonia_predict']]
    combined_df.set_index('date', inplace=True)
    return combined_df


def generate_daily_dataframe(combined_df):
    all_dates = pd.date_range(start=combined_df.index.min(), end=combined_df.index.max(), freq='D')
    daily_df = combined_df.reindex(all_dates)
    daily_df['liborusd_ov_predict'] = daily_df['liborusd_ov_predict'].ffill()
    daily_df['estereonia_predict'] = daily_df['estereonia_predict'].ffill()
    return daily_df
