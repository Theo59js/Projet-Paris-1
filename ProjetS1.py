
import pandas as pd
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Définir les chemins des fichiers input et output
input_path = 'C:/Users/theo5/OneDrive/Bureau/Bloomberg_extract.xlsx'
output_path = 'C:/Users/theo5/OneDrive/Bureau/'

# Charger le dataframe
bloom_df = pd.read_excel(input_path)

# Afficher les 5 premières lignes des données
print(bloom_df.head())
#%%
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
#%%
# Extraires les noms des colonnes
column_date = Columns[0]
column_ask = Columns[1]
#%%
# Afficher les 5 premières lignes du dataframe 'ester'
ester.head()
#%%
# Vérifier la correspondance entre ester et eonia
index = ester[ester[column_date] == '2021-12-31'].index.tolist()
if ester.loc[index,column_ask].equals(eonia.loc[index, column_ask]) :
    print("Correspondance OK")
else :
    sys.exit
#%%
# Concaténer 'ester' et 'eonia'
estereonia = pd.concat([ester, eonia], ignore_index=True)
#%%
# Supprimer les lignes avec des valeurs manquantes
estereonia = estereonia.dropna(how='all')

# Supprimer les doublons dans 'estereonia'
estereonia = estereonia.drop_duplicates(subset=column_date, keep='first').reset_index(drop=True)

print(estereonia)
#%%
# Créer un graphique et l'afficher
plt.plot(estereonia[column_date], estereonia[column_ask], label='ester Ask')
plt.plot(liborusd_3m[column_date], liborusd_3m[column_ask], label='liborusd_3m Ask')


plt.legend()
plt.title('Comparaison ESTER (EONIA avant 2019) et EURIBOR')
plt.xlabel('Date')
plt.ylabel('Valeur Ask')

plt.show()
#%%
# Convertir les colonnes 'Date' en format de date
eurusd[column_date] = pd.to_datetime(eurusd['Date'])
liborusd_ov[column_date] = pd.to_datetime(liborusd_ov['Date'])
estereonia[column_date] = pd.to_datetime(estereonia['Date'])

# Fusionner les dataframes sur la colonne "Date"
merged_df = pd.merge(eurusd, liborusd_3m, on='Date', how='inner')
merged_df = pd.merge(merged_df, estereonia, on='Date', how='inner')
print(merged_df.head)
#%%
# Fusionner les dataframes des variables explicatives
var_ex = merged_df.iloc[:, [2, 3]]
var_dep = merged_df.iloc[:, 1]

# Ajouter constante aux variables eplicatives pour l'intercept
var_ex = sm.add_constant(var_ex)

# Faire la régression et l'imprimer
regeurusd = sm.OLS(var_dep, var_ex).fit()
print(regeurusd.summary())
#%%
# Créer un DataFrame de nouvelles données, selon notre scénario Fed et BCE
predict_datas = pd.DataFrame({'liborusd_ov_predict': [5.65]*60 + [5.15]*90 + [4.90]*90,
                                'estereonia_predict': [3.90]*120 + [3.50]*120})
# On contrôle que notre dataframe s'est constitué correctement
print(predict_datas)
#%%
# Faire les prédictions pour notre scénario Fed et BCE
predict_datas_const = sm.add_constant(predict_datas)
predictions = regeurusd.predict(predict_datas_const)

# Afficher les prédictions EURUSD
print(predictions)
#%%
# Définir la date de départ
date_depart = pd.to_datetime('2023-11-29')

# Générer une séquence de dates pour les 240 jours suivants
dates_futures = pd.date_range(date_depart, periods=240)

# Fusionner la séries de prédictions avec les dates dans un dataframe
df_predictions = pd.DataFrame({'predictions': predictions.values}, index=dates_futures)

print(df_predictions)
#%%
# Faire un graphique pour afficher nos résultats
plt.figure(figsize=(10, 6))
plt.plot(df_predictions.index, df_predictions['predictions'], label='Prédictions', marker='o', linestyle='-', color='blue')

# Ajouter des titres et des étiquettes
plt.title('Prédictions EURUSD selon notre scénario')
plt.xlabel('Date')
plt.ylabel('Prédictions EURUSD')

# Afficher la légende
plt.legend()

# Exporter le graphique en PDF
pdf_path = output_path + 'Prédictions_EURUSD.pdf'
plt.savefig(pdf_path, format='pdf')

# Afficher le graphique
plt.show()
#%%
