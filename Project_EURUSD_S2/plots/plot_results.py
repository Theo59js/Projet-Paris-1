import matplotlib.pyplot as plt
import pandas as pd


def plot_predictions(predictions, pdf_path):
    predictions_df = pd.DataFrame(predictions, columns=['predictions'])

    plt.figure(figsize=(10, 6))
    plt.plot(predictions_df.index, predictions_df['predictions'], label='Prédictions',
             marker='o', linestyle='-', color='blue')

    plt.title('Prédictions EURUSD selon notre scénario')
    plt.xlabel('Date')
    plt.ylabel('Prédictions EURUSD')
    plt.legend()

    plt.savefig(pdf_path, format='pdf')
    plt.show()