import statsmodels.api as sm
import pandas as pd

from config import get_config
from data.data_loader import load_data
from gui.user_interface import launch_gui
from models.regression_model import train_model, make_predictions
from plots.plot_results import plot_predictions
from utils.data_processing import process_data


def main():
    config = get_config()

    # Charger les données
    bloom_df = load_data(config['input']['path'])

    # Traiter les données
    estereonia, liborusd_3m, eurusd = process_data(bloom_df)

    # Convertir les colonnes 'Date' en format de date
    eurusd['Date'] = pd.to_datetime(eurusd['Date'])
    liborusd_3m['Date'] = pd.to_datetime(liborusd_3m['Date'])
    estereonia['Date'] = pd.to_datetime(estereonia['Date'])

    # Fusionner les dataframes sur la colonne "Date"
    merged_df = pd.merge(eurusd, liborusd_3m, on='Date', how='inner')
    merged_df = pd.merge(merged_df, estereonia, on='Date', how='inner')

    # Entraîner le modèle
    regeurusd, var_ex = train_model(merged_df)

    # Lancer l'interface utilisateur pour obtenir les prédictions
    predict_datas = launch_gui()

    # Faire des prédictions
    if not predict_datas.empty:
        predict_datas_const = sm.add_constant(predict_datas)
        predictions = make_predictions(regeurusd, predict_datas_const)

        # Afficher les prédictions
        plot_predictions(predictions, config['output']['pdf_name'])
    else:
        print("Aucune donnée de prédiction saisie.")


if __name__ == "__main__":
    main()
