import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Daten laden
data = pd.read_csv('DuneMaster.csv')

# Filtern der Daten für verlorene Spiele
lost_games = data[data['is_winner'] == 0]

# Schritt 1: Berechnen des durchschnittlichen Verlusts pro Verlustrunde für jeden Spieler
average_loss_per_lost_round = lost_games.groupby('depositor')['deposit_usd'].mean().reset_index()
average_loss_per_lost_round.rename(columns={'deposit_usd': 'average_loss_per_lost_round'}, inplace=True)

# Schritt 2: Berechnen des durchschnittlichen Einsatzes in der Runde nach einer Verlustrunde für jeden Spieler
data_sorted = data.sort_values(by=['depositor', 'block_number'])
data_sorted['next_round_after_loss'] = data_sorted['is_winner'].shift(1) == 0
average_deposit_after_loss = data_sorted[data_sorted['next_round_after_loss']].groupby('depositor')['deposit_usd'].mean().reset_index()
average_deposit_after_loss.rename(columns={'deposit_usd': 'average_deposit_after_loss'}, inplace=True)

# Schritt 3: Zusammenführen der Daten für die Regression
merged_data_for_regression = pd.merge(average_loss_per_lost_round, average_deposit_after_loss, on='depositor')

# Regression
X = merged_data_for_regression['average_loss_per_lost_round']
y = merged_data_for_regression['average_deposit_after_loss']
X = sm.add_constant(X)  # Konstante hinzufügen

model = sm.OLS(y, X).fit()

# Grafik erstellen
plt.figure(figsize=(10, 6))
sns.regplot(x='average_loss_per_lost_round', y='average_deposit_after_loss', data=merged_data_for_regression, scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Regression of Average Deposit After Loss on Average Loss per Lost Round')
plt.xlabel('Average Loss per Lost Round (USD)')
plt.ylabel('Average Deposit After Loss (USD)')
plt.show()

# Zusammenfassung des Modells anzeigen
print(model.summary())
