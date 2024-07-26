import datetime
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

#                          #
# ----- QUERY PILOTI ----- #
#                          #

def get_most_drivers_championships():
    """
    Recupera i piloti con il maggior numero di campionati del mondo vinti.
    
    Returns:
        list: Una lista di dizionari contenente i piloti e il numero di campionati vinti.
    """
    # Recupera i dati dei piloti con driverId, forename e surname, escludendo _id
    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'forename': 1, 'surname': 1, '_id': 0})
    drivers = list(drivers_cursor)

    # Dizionario per tenere traccia dei punti per anno per ciascun pilota
    driver_yearly_points = defaultdict(lambda: defaultdict(int))
    driver_championships = defaultdict(int)

    # Recupera i risultati delle gare e le informazioni delle gare
    results_cursor = Results.collection.find({}, {'driverId': 1, 'points': 1, 'raceId': 1})
    results = list(results_cursor)

    races_cursor = Races.collection.find({}, {'raceId': 1, 'year': 1})
    races = {race['raceId']: race['year'] for race in races_cursor}

    for result in results:
        driver_id = result['driverId']
        points = result.get('points', 0)
        race_id = result['raceId']
        year = races.get(race_id, None)
        if year:
            driver_yearly_points[driver_id][year] += points

    # Determina il campione dell'anno
    yearly_champions = defaultdict(lambda: {'driverId': None, 'totalPoints': 0})

    for driver_id, years in driver_yearly_points.items():
        for year, points in years.items():
            if points > yearly_champions[year]['totalPoints']:
                yearly_champions[year]['totalPoints'] = points
                yearly_champions[year]['driverId'] = driver_id

    # Conta i campionati vinti da ciascun pilota
    for year_info in yearly_champions.values():
        driver_id = year_info['driverId']
        if driver_id:
            driver_championships[driver_id] += 1

    # Aggiunge il numero di campionati vinti ai dati dei piloti
    for driver in drivers:
        driver_id = driver['driverId']
        driver['championshipsWon'] = driver_championships.get(driver_id, 0)

    # Ordina i piloti per numero di campionati vinti in ordine decrescente
    top_drivers_by_championships = sorted(drivers, key=lambda x: x['championshipsWon'], reverse=True)

    # Restituisci i primi 20 piloti
    return top_drivers_by_championships[:10]


def get_most_drivers_wins():
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
    return winningest_drivers[:10]


def get_most_drivers_podiums():
    """
    Recupera i piloti con il maggior numero di podi (primi tre posti) e le percentuali di podi e i nomi dei costruttori separati da virgola.
    
    Returns:
        list: Una lista di dizionari contenente i piloti, il loro numero di podi, la percentuale di podi e i nomi dei costruttori separati da virgola.
    """
    # Recupera i dati dei piloti con driverId, forename e surname, escludendo _id
    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'forename': 1, 'surname': 1, '_id': 0})
    drivers = list(drivers_cursor)

    # Recupera i dati dei costruttori con constructorId e name, escludendo _id
    constructors_cursor = Constructors.collection.find({}, {'constructorId': 1, 'name': 1, '_id': 0})
    constructors = list(constructors_cursor)

    # Crea un dizionario per i nomi dei costruttori
    constructor_names = {constructor['constructorId']: constructor['name'] for constructor in constructors}

    # Dizionari per tenere traccia dei podi, delle gare e dei costruttori per ciascun pilota
    driver_podiums = defaultdict(int)
    driver_race_counts = defaultdict(int)
    driver_constructors = defaultdict(set)

    # Recupera i risultati delle gare per contare i podi e i costruttori
    results_cursor = Results.collection.find({'positionOrder': {'$lte': 3}}, {'driverId': 1, 'constructorId': 1, 'raceId': 1, '_id': 0})
    results = list(results_cursor)

    for result in results:
        driver_id = result['driverId']
        driver_podiums[driver_id] += 1
        driver_constructors[driver_id].add(result['constructorId'])

    # Recupera tutte le gare a cui hanno partecipato i piloti
    all_results_cursor = Results.collection.find({}, {'driverId': 1, 'raceId': 1, '_id': 0})
    all_results = list(all_results_cursor)

    for result in all_results:
        driver_race_counts[result['driverId']] += 1

    # Aggiunge i campi 'podiums', 'podiumPercentage' e 'constructors' per ciascun pilota nel risultato finale
    for driver in drivers:
        driver_id = driver['driverId']
        total_races = driver_race_counts.get(driver_id, 1)  # Evita la divisione per zero
        podiums = driver_podiums.get(driver_id, 0)
        podium_percentage = round((podiums / total_races) * 100, 2)
        constructors = ', '.join(constructor_names[constructor_id] for constructor_id in driver_constructors.get(driver_id, []))

        driver['podiums'] = podiums
        driver['podiumPercentage'] = podium_percentage
        driver['constructors'] = constructors

    # Ordina i piloti per numero di podi in ordine decrescente
    podium_drivers = sorted(drivers, key=lambda x: x['podiums'], reverse=True)

    # Restituisci i primi 10 piloti
    return podium_drivers[:10]


def get_most_drivers_points():
    """
    Recupera i piloti con il maggior numero di punti accumulati e calcola i punti per gara.
    
    Returns:
        list: Una lista di dizionari contenente i piloti, il totale dei punti, e la media dei punti per gara.
    """
    # Recupera i dati dei piloti con driverId, forename e surname, escludendo _id
    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'forename': 1, 'surname': 1, '_id': 0})
    drivers = list(drivers_cursor)

    # Dizionari per tenere traccia dei punti e delle gare dei piloti
    driver_points = defaultdict(int)
    driver_race_counts = defaultdict(int)

    # Recupera i risultati delle gare con i punti ottenuti da ciascun pilota
    results_cursor = Results.collection.find({}, {'driverId': 1, 'points': 1, '_id': 0})
    results = list(results_cursor)

    # Popola i dizionari con i punti e il numero di gare per ciascun pilota
    for result in results:
        driver_id = result['driverId']
        driver_points[driver_id] += result.get('points', 0)  # Usa 0 come valore predefinito se i punti non sono disponibili
        driver_race_counts[driver_id] += 1  # Conta ogni risultato come una gara

    # Aggiunge il totale dei punti e i punti per gara per ciascun pilota ai dati dei piloti
    for driver in drivers:
        driver_id = driver['driverId']
        total_points = driver_points.get(driver_id, 0)
        total_races = driver_race_counts.get(driver_id, 1)  # Evita la divisione per zero

        driver['totalPoints'] = total_points
        driver['pointsPerGP'] = round(total_points / total_races, 2)  # Calcola i punti per gara

    # Ordina i piloti per totale punti in ordine decrescente
    top_drivers_by_points = sorted(drivers, key=lambda x: x['totalPoints'], reverse=True)

    # Restituisci i primi 20 piloti
    return top_drivers_by_points[:10]


def get_most_driver_pole_positions():
    """
    Recupera i piloti con il maggior numero di pole position e la percentuale di pole position, 
    includendo i team con cui sono state raggiunte.

    Returns:
        list: Una lista di dizionari contenente i piloti, il numero di pole position, la percentuale di pole position
              e i team con cui sono state raggiunte.
    """
    # Recupera i dati dei piloti con driverId, forename e surname, escludendo _id
    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'forename': 1, 'surname': 1, '_id': 0})
    drivers = list(drivers_cursor)

    # Recupera i dati dei costruttori con constructorId e name, escludendo _id
    constructors_cursor = Constructors.collection.find({}, {'constructorId': 1, 'name': 1, '_id': 0})
    constructors = list(constructors_cursor)

    # Crea un dizionario per i nomi dei costruttori
    constructor_names = {constructor['constructorId']: constructor['name'] for constructor in constructors}

    # Dizionari per tenere traccia delle pole position, delle gare e dei costruttori per ciascun pilota
    driver_pole_positions = defaultdict(int)
    driver_race_counts = defaultdict(int)
    driver_constructors = defaultdict(set)

    # Recupera i risultati delle gare per contare le pole position (griglia di partenza = 1) e i costruttori
    results_cursor = Results.collection.find({}, {'driverId': 1, 'grid': 1, 'constructorId': 1, '_id': 0})
    results = list(results_cursor)

    # Conta le pole position e tiene traccia delle squadre per ciascun pilota
    for result in results:
        driver_id = result['driverId']
        driver_race_counts[driver_id] += 1  # Conta ogni risultato come una gara
        if result['grid'] == 1:
            driver_pole_positions[driver_id] += 1
            driver_constructors[driver_id].add(result['constructorId'])

    # Aggiunge il numero di pole position, la percentuale e i team ai dati dei piloti
    for driver in drivers:
        driver_id = driver['driverId']
        total_races = driver_race_counts.get(driver_id, 1)  # Evita la divisione per zero
        pole_positions = driver_pole_positions.get(driver_id, 0)
        pole_percentage = round((pole_positions / total_races) * 100, 2)
        constructors = ', '.join(constructor_names[constructor_id] for constructor_id in driver_constructors.get(driver_id, []))

        driver['polePositions'] = pole_positions
        driver['polePercentage'] = pole_percentage
        driver['constructors'] = constructors

    # Ordina i piloti per numero di pole position in ordine decrescente
    top_drivers_by_pole_positions = sorted(drivers, key=lambda x: x['polePositions'], reverse=True)

    # Restituisci i primi 20 piloti
    return top_drivers_by_pole_positions[:10]


#                               #
# ----- QUERY COSTRUTTORI ----- #
#                               #


def get_most_constructors_championships():
    """
    Recupera i costruttori con il maggior numero di campionati del mondo vinti.
    
    Returns:
        list: Una lista di dizionari contenente i costruttori e il numero di campionati vinti.
    """
    # Recupera i dati dei costruttori
    constructors_cursor = Constructors.collection.find({}, {'constructorId': 1, 'name': 1, '_id': 0})
    constructors = list(constructors_cursor)
    
    # Dizionario per tenere traccia dei punti per anno per ciascun costruttore
    constructor_yearly_points = defaultdict(lambda: defaultdict(int))
    constructor_championships = defaultdict(int)
    
    # Recupera i risultati dei costruttori e le informazioni delle gare
    constructor_standings_cursor = ConstructorStandings.collection.find({}, {'constructorId': 1, 'points': 1, 'raceId': 1, 'position': 1})
    constructor_standings = list(constructor_standings_cursor)
    
    races_cursor = Races.collection.find({}, {'raceId': 1, 'year': 1})
    races = {race['raceId']: race['year'] for race in races_cursor}

    # Calcola i punti totali per ciascun costruttore per anno
    for standing in constructor_standings:
        constructor_id = standing['constructorId']
        points = standing.get('points', 0)
        race_id = standing['raceId']
        year = races.get(race_id, None)
        if year and standing['position'] == 1:  # Considera solo i primi posti per determinare il campione dell'anno
            constructor_yearly_points[constructor_id][year] += points

    # Determina il campione dell'anno
    yearly_champions = defaultdict(lambda: {'constructorId': None, 'totalPoints': 0})

    for constructor_id, years in constructor_yearly_points.items():
        for year, points in years.items():
            if points > yearly_champions[year]['totalPoints']:
                yearly_champions[year]['totalPoints'] = points
                yearly_champions[year]['constructorId'] = constructor_id

    # Conta i campionati vinti da ciascun costruttore
    for year_info in yearly_champions.values():
        constructor_id = year_info['constructorId']
        if constructor_id:
            constructor_championships[constructor_id] += 1

    # Aggiunge il numero di campionati vinti ai dati dei costruttori
    for constructor in constructors:
        constructor_id = constructor['constructorId']
        constructor['championshipsWon'] = constructor_championships.get(constructor_id, 0)

    # Ordina i costruttori per numero di campionati vinti in ordine decrescente
    top_constructors_by_championships = sorted(constructors, key=lambda x: x['championshipsWon'], reverse=True)

    # Restituisci i primi 20 costruttori
    return top_constructors_by_championships[:10]


def get_most_constructors_wins():
    """
    Recupera i costruttori con il maggior numero di vittorie nelle gare e fornisce il numero di vittorie e le date della prima e dell'ultima gara vinta, mostrando solo l'anno.

    Returns:
        list: Una lista di dizionari contenente i costruttori, il numero totale di vittorie, l'anno della prima e dell'ultima gara vinta.
    """
    # Recupera i dati dei costruttori con constructorId e name, escludendo _id
    constructors_cursor = Constructors.collection.find({}, {'constructorId': 1, 'name': 1, '_id': 0})
    constructors = list(constructors_cursor)

    # Dizionari per tenere traccia delle vittorie e delle date delle vittorie per ciascun costruttore
    constructor_wins = defaultdict(list)

    # Recupera i risultati delle gare per contare le vittorie e le date delle gare dei costruttori
    results_cursor = Results.collection.find({'positionOrder': 1}, {'constructorId': 1, 'raceId': 1, '_id': 0})
    results = list(results_cursor)

    # Recupera le informazioni sulle gare, inclusi nome e data
    races_cursor = Races.collection.find({}, {'raceId': 1, 'name': 1, 'date': 1, '_id': 0})
    races = {race['raceId']: {'name': race['name'].replace(' Grand Prix', ' GP'), 'date': race['date']} for race in races_cursor}

    # Popola il dizionario con le date delle vittorie per ciascun costruttore
    for result in results:
        constructor_id = result['constructorId']
        race_info = races.get(result['raceId'])
        if race_info:
            constructor_wins[constructor_id].append(race_info)

    # Aggiunge i campi 'wins', 'firstWin' e 'lastWin' per ciascun costruttore nel risultato finale
    constructor_list = []
    for constructor in constructors:
        constructor_id = constructor['constructorId']
        wins_info = constructor_wins.get(constructor_id, [])
        wins_count = len(wins_info)

        if wins_info:
            wins_info_sorted = sorted(wins_info, key=lambda x: x['date'])
            first_win_year = wins_info_sorted[0]['date'].strftime('%Y')
            last_win_year = wins_info_sorted[-1]['date'].strftime('%Y')
            first_win = f"{wins_info_sorted[0]['name']} {first_win_year}"
            last_win = f"{wins_info_sorted[-1]['name']} {last_win_year}"
        else:
            first_win = None
            last_win = None

        constructor_list.append({
            'name': constructor['name'],
            'wins': wins_count,
            'firstWin': first_win,
            'lastWin': last_win
        })

    # Ordina i costruttori per numero di vittorie in ordine decrescente
    top_constructors_by_wins = sorted(constructor_list, key=lambda x: x['wins'], reverse=True)

    # Restituisci i primi 10 costruttori
    return top_constructors_by_wins[:10]


def get_most_constructor_podiums():
    """
    Recupera i costruttori con il maggior numero di podi (primi tre posti),
    includendo la percentuale di podi e il miglior pilota per ciascun team.
    
    Returns:
        list: Una lista di dizionari contenente i costruttori, il numero di podi,
              la percentuale di podi e il miglior pilota per ciascun team.
    """
    # Recupera i dati dei costruttori con constructorId e name, escludendo _id
    constructors_cursor = Constructors.collection.find({}, {'constructorId': 1, 'name': 1, '_id': 0})
    constructors = list(constructors_cursor)

    # Crea un dizionario per i nomi dei costruttori
    constructor_names = {constructor['constructorId']: constructor['name'] for constructor in constructors}

    # Dizionari per tenere traccia dei podi e delle gare per ciascun costruttore
    constructor_podiums = defaultdict(int)
    constructor_race_counts = defaultdict(int)
    constructor_driver_podiums = defaultdict(lambda: defaultdict(int))  # Aggiungi un dizionario per tenere traccia dei podi dei piloti

    # Recupera i dati delle classifiche costruttori per contare i podi (primi tre posti) e le gare
    constructor_standings_cursor = ConstructorStandings.collection.find({'position': {'$lte': 3}}, {'constructorId': 1, 'raceId': 1, 'position': 1})
    constructor_standings = list(constructor_standings_cursor)
    
    # Recupera le informazioni delle gare e dei piloti
    races_cursor = Races.collection.find({}, {'raceId': 1, '_id': 0})
    races = {race['raceId']: race for race in races_cursor}

    results_cursor = Results.collection.find({}, {'raceId': 1, 'constructorId': 1, 'driverId': 1, 'points': 1, '_id': 0})
    results = list(results_cursor)

    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'forename': 1, 'surname': 1, '_id': 0})
    drivers = {driver['driverId']: f"{driver['forename']} {driver['surname']}" for driver in drivers_cursor}

    # Conta i podi e le gare per ciascun costruttore
    for standing in constructor_standings:
        constructor_id = standing['constructorId']
        race_id = standing['raceId']
        
        constructor_podiums[constructor_id] += 1

    # Conta tutte le gare a cui hanno partecipato i costruttori
    all_constructor_standings_cursor = ConstructorStandings.collection.find({}, {'constructorId': 1, 'raceId': 1, '_id': 0})
    all_constructor_standings = list(all_constructor_standings_cursor)

    for standing in all_constructor_standings:
        constructor_id = standing['constructorId']
        constructor_race_counts[constructor_id] += 1

    # Conta i podi dei piloti per ciascun costruttore
    for result in results:
        race_id = result['raceId']
        constructor_id = result['constructorId']
        driver_id = result['driverId']
        position = result.get('position', 0)
        
        if position <= 3:  # Conta solo i podi (primi tre posti)
            constructor_driver_podiums[constructor_id][driver_id] += 1

    # Trova il miglior pilota per ciascun costruttore
    best_driver_by_constructor = {}
    for constructor_id, driver_podiums in constructor_driver_podiums.items():
        best_driver_id = max(driver_podiums, key=driver_podiums.get)
        best_driver_by_constructor[constructor_id] = drivers[best_driver_id]

    # Aggiunge i campi 'podiums', 'percentage_podiums', e 'best_driver' per ciascun costruttore nel risultato finale
    constructor_list = []
    for constructor_id, name in constructor_names.items():
        total_races = constructor_race_counts.get(constructor_id, 1)  # Evita la divisione per zero
        podiums = constructor_podiums.get(constructor_id, 0)
        percentage_podiums = round((podiums / total_races) * 100, 2) if total_races > 0 else 0
        best_driver = best_driver_by_constructor.get(constructor_id, 'Unknown')

        constructor_list.append({
            'name': name,
            'podiums': podiums,
            'percentage_podiums': percentage_podiums,
            'best_driver': best_driver
        })

    # Ordina i costruttori per numero di podi in ordine decrescente
    top_constructors_by_podiums = sorted(constructor_list, key=lambda x: x['podiums'], reverse=True)

    # Restituisci i primi 10 costruttori
    return top_constructors_by_podiums[:10]


def get_most_constructor_starts():
    """
    Recupera il numero di partenze in Grand Prix per ciascun costruttore e l'intervallo di stagioni attive per ciascun costruttore.

    Returns:
        list: Una lista di dizionari contenente i costruttori, il numero totale di partenze in Grand Prix
              e l'intervallo di stagioni attive per ogni costruttore.
    """

    # Recupera i dati delle gare e filtra solo le gare di Grand Prix
    races_cursor = Races.collection.find({}, {'raceId': 1, 'name': 1, 'year': 1, '_id': 0})
    races = list(races_cursor)
    grand_prix_races = {race['raceId'] for race in races if 'Grand Prix' in race['name']}
    grand_prix_years = {race['raceId']: race['year'] for race in races if 'Grand Prix' in race['name']}

    # Recupera i risultati delle gare di Grand Prix
    results_cursor = Results.collection.find({'raceId': {'$in': list(grand_prix_races)}}, {'raceId': 1, 'constructorId': 1, '_id': 0})
    results = list(results_cursor)

    # Recupera i dati dei costruttori
    constructors_cursor = Constructors.collection.find({}, {'constructorId': 1, 'name': 1, '_id': 0})
    constructors = {constructor['constructorId']: constructor['name'] for constructor in constructors_cursor}

    # Dizionari per tenere traccia delle partenze e delle stagioni
    constructor_participation = defaultdict(int)
    active_years = defaultdict(set)
    
    # Conta le partenze in Grand Prix per ciascun costruttore e registra gli anni
    for result in results:
        constructor_id = result['constructorId']
        race_id = result['raceId']
        if race_id in grand_prix_years:
            year = grand_prix_years[race_id]
            constructor_participation[constructor_id] += 1
            active_years[constructor_id].add(year)

    # Trova l'intervallo di stagioni attive per ciascun costruttore
    constructor_info = []
    for constructor_id, num_participations in constructor_participation.items():
        years_list = sorted(active_years[constructor_id])
        first_year = years_list[0] if years_list else 'Unknown'
        last_year = years_list[-1] if years_list else 'Unknown'
        if 2024 in years_list:
            active_seasons = f"{first_year} -"
        else:
            active_seasons = f"{first_year}-{last_year}" if years_list else 'Unknown'
        
        constructor_info.append({
            'constructor_id': constructor_id,
            'name': constructors.get(constructor_id, 'Unknown'),
            'num_participations': num_participations,
            'active_seasons': active_seasons
        })

    # Ordina i costruttori per numero di partenze in ordine decrescente
    sorted_constructors = sorted(constructor_info, key=lambda x: x['num_participations'], reverse=True)

    # Restituisci la lista ordinata
    return sorted_constructors[:10]


def get_constructor_fastest_laps():
    """
    Recupera il numero di giri più veloci per ciascun costruttore e i nomi del primo e dell'ultimo Gran Premio
    in cui il costruttore ha ottenuto il giro più veloce, inclusi gli anni.

    Returns:
        list: Una lista di dizionari contenente i costruttori, il numero totale di giri più veloci,
              e i nomi del primo e dell'ultimo Gran Premio con il giro più veloce, inclusi gli anni.
    """

    # Recupera i dati dei costruttori con constructorId e name, escludendo _id
    constructors_cursor = Constructors.collection.find({}, {'constructorId': 1, 'name': 1, '_id': 0})
    constructors = {constructor['constructorId']: constructor['name'] for constructor in constructors_cursor}

    # Dizionari per tenere traccia dei giri più veloci e delle gare per ciascun costruttore
    constructor_fastest_laps = defaultdict(lambda: {
        'count': 0,
        'races': []
    })

    # Recupera i risultati delle gare con il giro più veloce
    results_cursor = Results.collection.find({'positionOrder': 1, 'fastestLap': {'$exists': True}}, {'constructorId': 1, 'raceId': 1, '_id': 0})
    results = list(results_cursor)

    # Recupera le informazioni sulle gare, inclusi nome e data
    races_cursor = Races.collection.find({}, {'raceId': 1, 'name': 1, 'date': 1, '_id': 0})
    races = {race['raceId']: {'name': race['name'].replace(' Grand Prix', ' GP'), 'date': race['date'], 'year': race['date'].year} for race in races_cursor}

    # Conta i giri più veloci e registra le gare per ciascun costruttore
    for result in results:
        constructor_id = result['constructorId']
        race_info = races.get(result['raceId'])
        if race_info:
            constructor_data = constructor_fastest_laps[constructor_id]
            constructor_data['count'] += 1
            constructor_data['races'].append(race_info)

    # Trova i nomi del primo e dell'ultimo Gran Premio per ciascun costruttore, inclusi gli anni
    constructor_info = []
    for constructor_id, data in constructor_fastest_laps.items():
        races_info = sorted(data['races'], key=lambda x: x['date'])
        first_race = races_info[0] if races_info else None
        last_race = races_info[-1] if races_info else None
        
        first_race_name = f"{first_race['name']} ({first_race['year']})" if first_race else 'Unknown'
        last_race_name = f"{last_race['name']} ({last_race['year']})" if last_race else 'Unknown'

        constructor_info.append({
            'constructor_id': constructor_id,
            'name': constructors.get(constructor_id, 'Unknown'),
            'fastest_laps': data['count'],
            'first_race': first_race_name,
            'last_race': last_race_name
        })

    # Ordina i costruttori per numero di giri più veloci in ordine decrescente
    sorted_constructors = sorted(constructor_info, key=lambda x: x['fastest_laps'], reverse=True)

    # Restituisci la lista ordinata
    return sorted_constructors[:10]


#                         #
# ----- ALTRE QUERY ----- #
#                         #


def get_circuits_with_most_gp():
    """
    Recupera il numero di Gran Premi disputati per ciascun circuito, il nome del circuito,
    l'anno del primo e dell'ultimo Gran Premio, e ordina i circuiti in base al numero di gare.
    
    Returns:
        list: Una lista di dizionari contenente i circuiti e il numero di Gran Premi disputati, 
              ordinati per numero di gare in ordine decrescente, con nome del circuito e 
              anno del primo e ultimo GP.
    """
    
    # Recupera i dati necessari dalla tabella `races`
    races_cursor = Races.collection.find({}, {'circuitId': 1, 'date': 1, '_id': 0})
    races_results = list(races_cursor)
    
    # Dizionario per tenere traccia delle gare per ciascun circuito
    circuit_gps = defaultdict(lambda: {'count': 0, 'dates': []})
    
    # Conta il numero di Gran Premi e raccoglie le date per ciascun circuito
    for race in races_results:
        circuit_id = race['circuitId']
        race_date = race['date']
        circuit_gps[circuit_id]['count'] += 1
        circuit_gps[circuit_id]['dates'].append(race_date)
    
    # Recupera i nomi dei circuiti
    circuits_cursor = Circuits.collection.find({}, {'circuitId': 1, 'name': 1, '_id': 0})
    circuits_data = {circuit['circuitId']: circuit['name'] for circuit in circuits_cursor}

    # Prepara la lista dei risultati con i nomi dei circuiti e le date
    circuit_gps_count = []
    for circuit_id, data in circuit_gps.items():
        if data['dates']:
            first_gp_year = min(date.year for date in data['dates'])
            last_gp_year = max(date.year for date in data['dates'])
        else:
            first_gp_year = last_gp_year = 'Unknown'
        
        circuit_gps_count.append({
            'circuit_id': circuit_id,
            'name': circuits_data.get(circuit_id, 'Unknown'),
            'num_gps': data['count'],
            'first_gp_year': first_gp_year,
            'last_gp_year': last_gp_year
        })
    
    # Ordina i circuiti per numero di Gran Premi in ordine decrescente
    sorted_circuits = sorted(circuit_gps_count, key=lambda x: x['num_gps'], reverse=True)

    return sorted_circuits[:10]


def get_nations_with_most_wins():
    """
    Recupera il numero di nazioni con più Grand Prix vinti,
    e il numero dei piloti che li hanno vinti, insieme a tutti i piloti con il numero di vittorie per ogni nazione.

    Returns:
        list: Una lista di dizionari contenente le nazioni,
              il numero di Grand Prix vinti, il numero di piloti che li hanno vinti,
              e tutti i piloti con il loro numero di vittorie.
    """

    # Recupera i dati necessari
    results_cursor = Results.collection.find({}, {'raceId': 1, 'driverId': 1, 'position': 1, '_id': 0})
    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'nationality': 1, 'surname': 1, '_id': 0})

    results = list(results_cursor)
    drivers = {driver['driverId']: (driver['nationality'], driver['surname']) for driver in drivers_cursor}

    # Dizionari per tenere traccia delle vittorie
    country_wins = defaultdict(int)
    country_drivers = defaultdict(set)
    driver_wins = defaultdict(int)

    # Conta le vittorie e registra i piloti per ciascuna nazione
    for result in results:
        if result['position'] == 1:  # Vittoria
            driver_id = result['driverId']
            nationality, surname = drivers.get(driver_id, ('Unknown', 'Unknown'))
            country_wins[nationality] += 1
            country_drivers[nationality].add(driver_id)
            driver_wins[driver_id] += 1

    # Crea la lista di informazioni per ciascuna nazione
    country_info = []
    for country, wins in country_wins.items():
        num_drivers = len(country_drivers[country])
        # Ordina i piloti per numero di vittorie in ordine decrescente
        sorted_drivers = sorted(((driver_id, drivers[driver_id][1], driver_wins[driver_id])
                                 for driver_id in country_drivers[country]),
                                key=lambda x: x[2], reverse=True)
        # Format the driver info as "surname (wins)"
        drivers_str = ", ".join(f"{surname} ({wins})" for _, surname, wins in sorted_drivers)
        country_info.append({
            'country': country,
            'num_wins': wins,
            'num_drivers': num_drivers,
            'drivers': drivers_str
        })

    # Ordina le nazioni per numero di vittorie in ordine decrescente
    sorted_countries = sorted(country_info, key=lambda x: x['num_wins'], reverse=True)

    # Restituisci la lista ordinata
    return sorted_countries[:10]


def get_nations_with_most_drivers():
    """
    Recupera il numero di nazioni con più piloti, il numero di Grand Prix vinti per ogni nazione,
    e il pilota più vincente per ciascuna nazione.

    Returns:
        list: Una lista di dizionari contenente le informazioni per ciascuna nazione.
    """

    # Recupera i dati necessari
    drivers_cursor = Drivers.collection.find({}, {'driverId': 1, 'nationality': 1, 'forename': 1, 'surname': 1, '_id': 0})
    results_cursor = Results.collection.find({}, {'raceId': 1, 'driverId': 1, 'position': 1, '_id': 0})

    drivers = list(drivers_cursor)
    results = list(results_cursor)

    # Dizionari per tenere traccia delle nazioni e dei vincitori
    nation_drivers = defaultdict(set)
    nation_wins = defaultdict(int)
    driver_wins = defaultdict(int)
    driver_nationality = {}

    # Converti la lista dei piloti in un dizionario per un accesso più veloce
    drivers_dict = {driver['driverId']: driver for driver in drivers}

    # Conta il numero di piloti per nazione e le vittorie per nazione
    for driver in drivers:
        nationality = driver['nationality']
        driver_id = driver['driverId']
        driver_nationality[driver_id] = nationality
        nation_drivers[nationality].add(driver_id)

    for result in results:
        driver_id = result['driverId']
        position = result.get('position', 0)

        if position == 1:  # Solo vittorie
            nationality = driver_nationality.get(driver_id, 'Unknown')
            nation_wins[nationality] += 1
            driver_wins[driver_id] += 1

    # Trova il pilota più vincente per ciascuna nazione
    nationality_best_driver = {}
    for driver_id, wins in driver_wins.items():
        nationality = driver_nationality.get(driver_id, 'Unknown')
        if nationality not in nationality_best_driver or driver_wins[driver_id] > driver_wins[nationality_best_driver[nationality]]:
            nationality_best_driver[nationality] = driver_id

    # Organizza i dati per la restituzione
    nation_info = []
    for nationality, drivers_set in nation_drivers.items():
        num_drivers = len(drivers_set)
        total_wins = nation_wins[nationality]
        best_driver_id = nationality_best_driver.get(nationality, None)
        best_driver_name = f"{drivers_dict.get(best_driver_id, {}).get('forename', 'Unknown')} {drivers_dict.get(best_driver_id, {}).get('surname', 'Unknown')}" if best_driver_id else 'Unknown'

        nation_info.append({
            'nationality': nationality,
            'num_drivers': num_drivers,
            'total_wins': total_wins,
            'best_driver': best_driver_name
        })

    # Ordina le nazioni per numero di piloti in ordine decrescente
    sorted_nations = sorted(nation_info, key=lambda x: x['num_drivers'], reverse=True)

    return sorted_nations[:10]




def generate_history_data():
    return {
        'mostChampionships': get_most_drivers_championships(),
        'mostWins': get_most_drivers_wins(),
        'podiums': get_most_drivers_podiums(),
        'mostPoints': get_most_drivers_points(),
        'polePositions': get_most_driver_pole_positions(),

        'mostConstructorChampionships': get_most_constructors_championships(),
        'mostConstructorsWins': get_most_constructors_wins(),
        'mostConstructorsPodiums': get_most_constructor_podiums(),
        'mostConstructorsStarts': get_most_constructor_starts(),
        'mostConstructorsFastLaps': get_constructor_fastest_laps(),

        'mostCircuitsGP': get_circuits_with_most_gp(),
        'mostNationsWins': get_nations_with_most_wins(),
        'mostNationsDrivers': get_nations_with_most_drivers()
    }