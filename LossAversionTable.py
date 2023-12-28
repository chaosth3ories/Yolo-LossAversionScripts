import pandas as pd

# Laden der Daten aus der Datei
data = pd.read_csv('DuneMaster.csv')

# Berechnung der Gesamteinsätze pro Runde in ETH
total_deposit_per_round = data.groupby('roundid')['deposit_eth'].sum()

# Hinzufügen der Gesamteinsätze zu den Daten
data = data.merge(total_deposit_per_round.rename('total_deposit_round'), on='roundid')

# Berechnung der Gewinnwahrscheinlichkeit und des möglichen Gewinns für jede Runde in ETH
data['win_probability'] = data['deposit_eth'] / data['total_deposit_round']
data['potential_win'] = data['total_deposit_round'] - data['deposit_eth']

# Verschieben der Daten um eine Runde, um Vergleiche zu ermöglichen
data['next_round_win_probability'] = data.groupby('depositor')['win_probability'].shift(-1)
data['next_round_potential_win'] = data.groupby('depositor')['potential_win'].shift(-1)
data['prev_round_deposit_eth'] = data.groupby('depositor')['deposit_eth'].shift(1)

# Bestimmung der Spieler, die die Bedingungen erfüllen
condition = (data['next_round_win_probability'] > 1.5 * data['win_probability']) & \
            (data['next_round_potential_win'] > data['prev_round_deposit_eth'])
players_meeting_condition = data[condition]

# Anzahl der Spieler, die die Bedingung erfüllen
players_count = players_meeting_condition['depositor'].nunique()

# Berechnung der durchschnittlichen Wettbeträge in ETH, Gewinn/Verlust und gespielten Runden für diese Spieler
average_deposit = players_meeting_condition['deposit_eth'].mean()
average_win_loss = players_meeting_condition.apply(
    lambda row: -row['deposit_eth'] if row['is_winner'] == 0 else (players_meeting_condition[players_meeting_condition['roundid'] == row['roundid']]['deposit_eth'].sum() - row['deposit_eth']),
    axis=1
).mean()
average_rounds_played = players_meeting_condition.groupby('depositor')['roundid'].nunique().mean()

# Ausgabe der Ergebnisse
print(f"Anzahl der Spieler: {players_count}")
print(f"Durchschnittlicher Wettbetrag in ETH: {average_deposit}")
print(f"Durchschnittlicher Gewinn/Verlust in ETH: {average_win_loss}")
print(f"Durchschnittliche Anzahl gespielter Runden: {average_rounds_played}")
