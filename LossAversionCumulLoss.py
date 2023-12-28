import pandas as pd
import matplotlib.pyplot as plt

# Laden der Daten
df = pd.read_csv('DuneMaster.csv')

# Sortieren der Daten nach Spieler und Runden
df_sorted = df.sort_values(by=['depositor', 'roundid'])

# Berechnen des kumulierten Verlusts
df_sorted['loss'] = df_sorted['deposit_usd'].where(df_sorted['is_winner'] == 0, 0)
df_sorted['cumulative_loss'] = df_sorted.groupby('depositor')['loss'].cumsum()

# Berechnen der nächsten Einsätze
df_sorted['next_bet'] = df_sorted.groupby('depositor')['deposit_usd'].shift(-1)

# Filtern auf Spiele, die nach einem Verlust gespielt wurden
df_after_loss = df_sorted[df_sorted['is_winner'] == 0]

# Gruppieren und Berechnen des Durchschnitts des nächsten Einsatzes nach kumulierten Verlusten
average_bets_after_loss = df_after_loss.groupby('cumulative_loss')['next_bet'].mean().reset_index()

# Erstellen des Liniencharts
plt.figure(figsize=(12, 6))
plt.plot(average_bets_after_loss['cumulative_loss'], average_bets_after_loss['next_bet'], linestyle='-', color='blue')
plt.xlabel('Kumulierter Verlust (USD)', fontsize=12)
plt.ylabel('Durchschnittlicher Einsatz nach Verlust (USD)', fontsize=12)
plt.title('Durchschnittliche Einsatzhöhen nach kumulativen Verlusten', fontsize=14)
plt.grid(True)
plt.show()
