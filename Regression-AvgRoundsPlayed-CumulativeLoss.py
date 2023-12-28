import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Daten laden
data = pd.read_csv('DuneMaster.csv')

# Berechnen der Anzahl an gespielten Runden für jeden Spieler
total_rounds_played = data.groupby('depositor')['roundid'].count().reset_index()
total_rounds_played.rename(columns={'roundid': 'total_rounds_played'}, inplace=True)

# Berechnen des kumulativen Verlusts für jeden Spieler
cumulative_loss = data[data['is_winner'] == 0].groupby('depositor')['deposit_usd'].sum().reset_index()
cumulative_loss.rename(columns={'deposit_usd': 'cumulative_loss'}, inplace=True)

# Zusammenführen der Daten für die Regression
merged_data_for_regression = pd.merge(total_rounds_played, cumulative_loss, on='depositor')

# Regression
X = merged_data_for_regression['cumulative_loss']
y = merged_data_for_regression['total_rounds_played']
X = sm.add_constant(X)  # Konstante hinzufügen
model = sm.OLS(y, X).fit()

# Grafik mit begrenzten Achsen erstellen
plt.figure(figsize=(10, 6))
sns.regplot(x='cumulative_loss', y='total_rounds_played', data=merged_data_for_regression, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.xlim(0, merged_data_for_regression['cumulative_loss'].quantile(0.95))  # Begrenzung der x-Achse auf das 95% Quantil
plt.ylim(0, merged_data_for_regression['total_rounds_played'].quantile(0.95))  # Begrenzung der y-Achse auf das 95% Quantil
plt.title('Regression of Total Rounds Played on Cumulative Loss (Limited Axes)')
plt.xlabel('Cumulative Loss (USD)')
plt.ylabel('Total Rounds Played')
plt.show()
