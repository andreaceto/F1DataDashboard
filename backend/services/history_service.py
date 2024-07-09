import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from services.common_service import TEAM_C, DRIVER_C, DRIVER_LS, LINESTYLES
from data.model import *
import os
import pandas as pd
from collections import defaultdict
from data.model import Drivers, Results, Races

def get_history():
    """
    Recupera i dati storici dei piloti.

    Returns:
        list: Una lista di dizionari contenente i dati storici.
    """
    # Recupera i dati dei piloti con driverId, forename e surname, escludendo _id
    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'forename': 1, 'surname': 1, '_id': 0})
    drivers = list(drivers_cursor)

    # Dizionario per tenere traccia delle vittorie dei piloti
    driver_gp_wins = defaultdict(list)

    # Recupera i risultati delle gare per contare le vittorie
    results_cursor = Results.collection.find({'positionOrder': 1}, {'driverId': 1, 'raceId': 1, '_id': 0})
    results = list(results_cursor)

    # Recupera le informazioni sulle gare, inclusi name e date
    races_cursor = Races.collection.find({}, {'raceId': 1, 'name': 1, 'date': 1, '_id': 0})
    races = {race['raceId']: {'name': race['name'].replace(' Grand Prix', ' GP'), 'date': race['date']} for race in races_cursor}

    # Popola il dizionario con il numero di Gran Premi vinti dai piloti
    for result in results:
        race_info = races[result['raceId']]
        driver_gp_wins[result['driverId']].append({'name': race_info['name'], 'date': race_info['date']})

    # Aggiunge i campi 'gpWins', 'firstWin', 'lastWin' per ciascun pilota nel risultato finale
    for driver in drivers:
        driver_id = driver['driverId']
        wins = driver_gp_wins.get(driver_id, [])
        driver['gpWins'] = len(wins)
        
        if wins:
            # Ordina le vittorie per data
            wins_sorted = sorted(wins, key=lambda x: x['date'])
            driver['firstWin'] = f"{wins_sorted[0]['name']} {wins_sorted[0]['date'].strftime('%y')}"
            driver['lastWin'] = f"{wins_sorted[-1]['name']} {wins_sorted[-1]['date'].strftime('%y')}"
        else:
            driver['firstWin'] = None
            driver['lastWin'] = None

    # Ordina i piloti per numero di Gran Premi vinti in ordine decrescente
    winningest_drivers = sorted(drivers, key=lambda x: x['gpWins'], reverse=True)

    # Restituisci i primi 20 piloti
    return winningest_drivers[:20]


