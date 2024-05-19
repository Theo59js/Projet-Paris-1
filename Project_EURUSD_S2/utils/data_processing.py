import pandas as pd


def process_data(bloom_df):
    try:
        # Créer des dataframes pour chaque entité
        liborusd_ov = bloom_df.iloc[:, [1, 2]].copy()
        liborusd_3m = bloom_df.iloc[:, [4, 5]].copy()
        euribor_3m = bloom_df.iloc[:, [7, 8]].copy()
        eonia = bloom_df.iloc[:, [10, 11]].copy()
        ester = bloom_df.iloc[:, [13, 14]].copy()
        eurusd = bloom_df.iloc[:, [16, 17]].copy()

        # Renommer les colonnes des dataframes
        columns: list[str] = ['Date', 'Ask']
        liborusd_ov.columns = columns
        liborusd_3m.columns = columns
        euribor_3m.columns = columns
        eonia.columns = columns
        ester.columns = columns
        eurusd.columns = columns

        # Vérifier la correspondance entre ester et eonia
        index = ester[ester['Date'] == '2021-12-31'].index.tolist()
        if ester.loc[index, 'Ask'].equals(eonia.loc[index, 'Ask']):
            print("Correspondance OK")
        else:
            print("Pas de correspondance")
            return None

        # Concaténer 'ester' et 'eonia'
        estereonia = pd.concat([ester, eonia], ignore_index=True)

        # Supprimer les lignes avec des valeurs manquantes
        estereonia = estereonia.dropna(how='all')

        # Supprimer les doublons dans 'estereonia'
        estereonia = estereonia.drop_duplicates(subset='Date', keep='first').reset_index(drop=True)

        return estereonia, liborusd_3m, eurusd

    except Exception as e:
        print(f"Error processing data: {e}")
        return None


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
