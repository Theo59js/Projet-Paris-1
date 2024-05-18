
import pandas as pd
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import tkinter as tk
from tkinter import ttk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Définir les chemins des fichiers input et output
input_path = 'C:/Users/theo5/OneDrive/Bureau/Bloomberg_extract.xlsx'
output_path = 'C:/Users/theo5/OneDrive/Bureau/'

# Charger le dataframe
bloom_df = pd.read_excel(input_path)

# Afficher les 5 premières lignes des données
print(bloom_df.head())

# Créer des dataframes pour chaque entité
liborusd_ov = bloom_df.iloc[:, [1, 2]].copy()
liborusd_3m = bloom_df.iloc[:, [4, 5]].copy()
euribor_3m = bloom_df.iloc[:, [7, 8]].copy()
eonia = bloom_df.iloc[:, [10, 11]].copy()
ester = bloom_df.iloc[:, [13, 14]].copy()
eurusd = bloom_df.iloc[:, [16, 17]].copy()

# Renommer les colonnes des dataframes
Columns = ['Date', 'Ask']
liborusd_ov.columns = Columns
liborusd_3m.columns = Columns
euribor_3m.columns = Columns
eonia.columns = Columns
ester.columns = Columns
eurusd.columns = Columns

# Afficher les 5 premières lignes des dataframes
print("liborusd_ov")
print(liborusd_ov.head())

print("liborusd_3m")
print(liborusd_3m.head())

print("euribor_3m")
print(euribor_3m.head())

print("eonia")
print(eonia.head())

print("ester")
print(ester.head())

print("eurusd")
print(eurusd.head())

# Extraires les noms des colonnes
column_date = Columns[0]
column_ask = Columns[1]

# Afficher les 5 premières lignes du dataframe 'ester'
ester.head()

# Vérifier la correspondance entre ester et eonia
index = ester[ester[column_date] == '2021-12-31'].index.tolist()
if ester.loc[index, column_ask].equals(eonia.loc[index, column_ask]):
    print("Correspondance OK")
else:
    sys.exit

# Concaténer 'ester' et 'eonia'
estereonia = pd.concat([ester, eonia], ignore_index=True)

# Supprimer les lignes avec des valeurs manquantes
estereonia = estereonia.dropna(how='all')

# Supprimer les doublons dans 'estereonia'
estereonia = estereonia.drop_duplicates(subset=column_date, keep='first').reset_index(drop=True)

print(estereonia)

# Créer un graphique et l'afficher
plt.plot(estereonia[column_date], estereonia[column_ask], label='ester Ask')
plt.plot(liborusd_3m[column_date], liborusd_3m[column_ask], label='liborusd_3m Ask')


plt.legend()
plt.title('Comparaison ESTER (EONIA avant 2019) et EURIBOR')
plt.xlabel('Date')
plt.ylabel('Valeur Ask')

plt.show()

# Convertir les colonnes 'Date' en format de date
eurusd[column_date] = pd.to_datetime(eurusd['Date'])
liborusd_ov[column_date] = pd.to_datetime(liborusd_ov['Date'])
estereonia[column_date] = pd.to_datetime(estereonia['Date'])

# Fusionner les dataframes sur la colonne "Date"
merged_df = pd.merge(eurusd, liborusd_3m, on='Date', how='inner')
merged_df = pd.merge(merged_df, estereonia, on='Date', how='inner')
print(merged_df.head)

# Fusionner les dataframes des variables explicatives
var_ex = merged_df.iloc[:, [2, 3]]
var_dep = merged_df.iloc[:, 1]

# Ajouter constante aux variables eplicatives pour l'intercept
var_ex = sm.add_constant(var_ex)

# Faire la régression et l'imprimer
regeurusd = sm.OLS(var_dep, var_ex).fit()
print(regeurusd.summary())

# Créer un DataFrame de nouvelles données, selon notre scénario Fed et BCE
#predict_datas = pd.DataFrame({'liborusd_ov_predict': [5.65]*60 + [5.15]*90 + [4.90]*90,

#    'estereonia_predict': [3.90]*120 + [3.50]*120})
# On contrôle que notre dataframe s'est constitué correctement
#print(predict_datas)

# Déclarer predict_datas comme une variable globale
predict_datas = None
def create_dataframe(libor_data, ester_data):
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

def submit_data():
    global predict_datas
    libor_values = [float(liborusd_ov_entry1.get()), float(liborusd_ov_entry2.get()), float(liborusd_ov_entry3.get())]
    libor_dates = [libor_date_entry1.get(), libor_date_entry2.get(), libor_date_entry3.get()]
    ester_values = [float(estereonia_entry1.get()), float(estereonia_entry2.get()), float(estereonia_entry3.get())]
    ester_dates = [ester_date_entry1.get(), ester_date_entry2.get(), ester_date_entry3.get()]
    libor_data = {'values': libor_values, 'dates': libor_dates}
    ester_data = {'values': ester_values, 'dates': ester_dates}
    user_predict_datas = create_dataframe(libor_data, ester_data)
    predict_datas = generate_daily_dataframe(user_predict_datas)
    print("DataFrame créé avec succès :\n", predict_datas)

root = tk.Tk()
root.title("Entrée de données")
liborusd_ov_label = ttk.Label(root, text="Libor USD Overnight:")
liborusd_ov_label.grid(row=0, column=0, padx=5, pady=5)
liborusd_ov_entry1 = ttk.Entry(root)
liborusd_ov_entry1.grid(row=0, column=1, padx=5, pady=5)
libor_date_label = ttk.Label(root, text="Date (jj/mm/aaaa):")
libor_date_label.grid(row=0, column=2, padx=5, pady=5)
libor_date_entry1 = ttk.Entry(root)
libor_date_entry1.grid(row=0, column=3, padx=5, pady=5)
liborusd_ov_entry2 = ttk.Entry(root)
liborusd_ov_entry2.grid(row=1, column=1, padx=5, pady=5)
libor_date_entry2 = ttk.Entry(root)
libor_date_entry2.grid(row=1, column=3, padx=5, pady=5)
liborusd_ov_entry3 = ttk.Entry(root)
liborusd_ov_entry3.grid(row=2, column=1, padx=5, pady=5)
libor_date_entry3 = ttk.Entry(root)
libor_date_entry3.grid(row=2, column=3, padx=5, pady=5)
estereonia_label = ttk.Label(root, text="ESTER (Eonia) Rate:")
estereonia_label.grid(row=3, column=0, padx=5, pady=5)
estereonia_entry1 = ttk.Entry(root)
estereonia_entry1.grid(row=3, column=1, padx=5, pady=5)
ester_date_label = ttk.Label(root, text="Date (jj/mm/aaaa):")
ester_date_label.grid(row=3, column=2, padx=5, pady=5)
ester_date_entry1 = ttk.Entry(root)
ester_date_entry1.grid(row=3, column=3, padx=5, pady=5)
estereonia_entry2 = ttk.Entry(root)
estereonia_entry2.grid(row=4, column=1, padx=5, pady=5)
ester_date_entry2 = ttk.Entry(root)
ester_date_entry2.grid(row=4, column=3, padx=5, pady=5)
estereonia_entry3 = ttk.Entry(root)
estereonia_entry3.grid(row=5, column=1, padx=5, pady=5)
ester_date_entry3 = ttk.Entry(root)
ester_date_entry3.grid(row=5, column=3, padx=5, pady=5)
submit_button = ttk.Button(root, text="Soumettre", command=submit_data)
submit_button.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
root.mainloop()

predict_datas_const = sm.add_constant(predict_datas)
predictions = regeurusd.predict(predict_datas_const)

# Convertir les prédictions en DataFrame
predictions_df = pd.DataFrame(predictions, index=predict_datas.index, columns=['predictions'])

# Afficher les prédictions EURUSD
print(predictions_df)

# Faire un graphique pour afficher nos résultats
plt.figure(figsize=(10, 6))
plt.plot(predictions_df.index, predictions_df['predictions'], label='Prédictions', marker='o', linestyle='-', color='blue')

# Ajouter des titres et des étiquettes
plt.title('Prédictions EURUSD selon notre scénario')
plt.xlabel('Date')
plt.ylabel('Prédictions EURUSD')

# Afficher la légende
plt.legend()

# Exporter le graphique en PDF
pdf_path = 'Prédictions_EURUSD.pdf'  # Assurez-vous de définir le chemin de sortie correctement
plt.savefig(pdf_path, format='pdf')

# Afficher le graphique
plt.show()

