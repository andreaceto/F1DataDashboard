import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from services.common_service import TEAM_C, DRIVER_C, DRIVER_LS, LINESTYLES
from data.model import *
import os

def get_calendar(year):
    """
    Recupera i nomi delle gare, le rispettive località e i periodi per l'anno specificato (2024), ordinati per data.

    Returns:
        list: Una lista di dizionari, ciascuno contenente il nome della gara, la località e il periodo (da fp1_date a date), ordinati per data.
    """
    races = list(Races.collection.find({'year': year}, {'name': 1, 'fp1_date': 1, 'date': 1, 'circuitId': 1, '_id': 0}).sort('date'))
    
    # Dizionario per mappare i nomi delle gare alle loro località speciali
    special_locations = {
        'Spanish Grand Prix': 'Barcelona',
        'Singapore Grand Prix': 'Singapore',
        'Qatar Grand Prix': 'Lusail',
        'Abu Dhabi Grand Prix': 'Yas Marina',
        'Monaco Grand Prix': 'Monaco'
    }
    
    race_flags = {
    'Bahrain Grand Prix': 'bahrain.png',
    'Saudi Arabian Grand Prix': 'saudiarabia.png',
    'Australian Grand Prix': 'australia.png',
    'Japanese Grand Prix': 'japan.png',
    'Chinese Grand Prix': 'china.png',
    'Miami Grand Prix': 'usa.png',
    'Emilia Romagna Grand Prix': 'italy.png',
    'Monaco Grand Prix': 'monaco.png',
    'Canadian Grand Prix': 'canada.png',
    'Spanish Grand Prix': 'spain.png',
    'Austrian Grand Prix': 'austria.png',
    'British Grand Prix': 'uk.png',
    'Hungarian Grand Prix': 'hungary.png',
    'Belgian Grand Prix': 'belgium.png',
    'Dutch Grand Prix': 'netherlands.png',
    'Italian Grand Prix': 'italy.png',
    'Azerbaijan Grand Prix': 'azerbaijan.png',
    'Singapore Grand Prix': 'singapore.png',
    'United States Grand Prix': 'usa.png',
    'Mexico City Grand Prix': 'mexico.png',
    'São Paulo Grand Prix': 'brazil.png',
    'Las Vegas Grand Prix': 'usa.png', 
    'Qatar Grand Prix': 'qatar.png',
    'Abu Dhabi Grand Prix': 'abudhabi.png'
}

    race_periods = []
    for race in races:
        # Verifica se il nome della gara è in special_locations, altrimenti recupera dal database
        location = special_locations.get(race['name'], None)
        if location is None:
            # Recupera le informazioni sulla località dal circuito
            circuit_info = Circuits.collection.find_one({'circuitId': race['circuitId']}, {'location': 1, '_id': 0})
            location = circuit_info['location'] if circuit_info else 'N/D'  # Se non ci sono informazioni sulla località, usa 'N/D'
        
        # Recupera il nome del file della bandiera per la gara corrente
        flag_filename = race_flags.get(race['name'], 'default.png')  # Se non trova il nome, usa 'default.png' come fallback
        
        # Costruisci il dizionario per ogni gara
        race_dict = {
            'name': race['name'].replace(' Grand Prix', ' GP'),
            'date': f"{race['fp1_date']} - {race['date']}",
            'location': location,
            'flag': f"/flags/{flag_filename}"  # Percorso dell'immagine della bandiera nella cartella 'public'
        }
        race_periods.append(race_dict)
    
    return race_periods
