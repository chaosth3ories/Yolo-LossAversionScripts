import pandas as pd

# Daten laden
data = pd.read_csv('DuneMaster.csv')

# Schritt 1: Identifizieren der ersten Gewinnrunde für jeden Spieler
first_win_round = data[data['is_winner'] == 1].groupby('depositor')['block_number'].min().reset_index()
first_win_round.rename(columns={'block_number': 'first_win_block_number'}, inplace=True)

# Schritt 2: Filtern der Daten für Runden vor der ersten Gewinnrunde für jeden Spieler
data_with_first_win = pd.merge(data, first_win_round, on='depositor')
data_before_first_win = data_with_first_win[data_with_first_win['block_number'] <= data_with_first_win['first_win_block_number']]

# Schritt 3: Berechnen des kumulierten Verlusts bis zur ersten Gewinnrunde für jeden Spieler
cumulative_loss_before_first_win = data_before_first_win[data_before_first_win['is_winner'] == 0].groupby('depositor')['deposit_usd'].sum().reset_index()

# Schritt 4: Berechnen des Durchschnitts und Medians des kumulierten Verlusts
average_cumulative_loss = cumulative_loss_before_first_win['deposit_usd'].mean()
median_cumulative_loss = cumulative_loss_before_first_win['deposit_usd'].median()

# Ausgabe der Ergebnisse
print("Durchschnittlicher kumulierter Verlust pro Spieler bis zur ersten Gewinnrunde: {:.2f} USD".format(average_cumulative_loss))
print("Median des kumulierten Verlusts pro Spieler bis zur ersten Gewinnrunde: {:.2f} USD".format(median_cumulative_loss))
