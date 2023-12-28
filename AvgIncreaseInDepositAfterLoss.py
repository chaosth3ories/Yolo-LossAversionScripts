import pandas as pd

# Laden der Daten
df = pd.read_csv('DuneMaster.csv')

# Sortieren der Daten nach Spieler und Runden
df_sorted = df.sort_values(by=['depositor', 'roundid'])

# Identifizieren der Verluste und berechnen des nächsten Einsatzes
df_sorted['loss'] = df_sorted['deposit_usd'].where(df_sorted['is_winner'] == 0, 0)
df_sorted['next_bet'] = df_sorted.groupby('depositor')['deposit_usd'].shift(-1)

# Filtern auf Spiele, die nach einem Verlust gespielt wurden
df_after_loss = df_sorted[df_sorted['is_winner'] == 0]

# Berechnen der Durchschnittswerte für Verlust und nächsten Einsatz pro Spieler
average_loss_and_bet = df_after_loss.groupby('depositor').agg({
    'loss': 'mean',
    'next_bet': 'mean'
}).dropna()

# Berechnen des prozentualen Unterschieds
average_loss_and_bet['percent_change'] = ((average_loss_and_bet['next_bet'] - average_loss_and_bet['loss']) / average_loss_and_bet['loss']) * 100

# Berechnen des durchschnittlichen prozentualen Unterschieds
average_percent_change = average_loss_and_bet['percent_change'].mean()

print(f"Durchschnittliche prozentuale Veränderung des Einsatzes nach einem Verlust: {average_percent_change:.2f}%")
