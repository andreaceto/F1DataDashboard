from data.model import Races, Circuits, Results, Status, SprintResults, Qualifying
from services.common_service import *
from datetime import datetime

def get_calendar(year):
    """
    Fetches the race calendar for the specified season year, including session details for each race.
    
    Args:
        year (int): The year of the season.

    Returns:
        list: A list of race dictionaries for the specified year.
    """
    races = list(Races.collection.find({'year': year}, {'_id': 0}).sort('round'))
    
    for race in races:
        sessions = []
        if race.get('fp1_date') != r'\N' and race.get('fp1_time') != r'\N':
            sessions.append({'type': 'FP1', 'date': race['fp1_date'], 'time': race['fp1_time']})
        if race.get('fp2_date') != r'\N' and race.get('fp2_time') != r'\N':
            session_type = 'Sprint Shootout' if race.get('sprint_date') != r'\N' else 'FP2'
            sessions.append({'type': session_type, 'date': race['fp2_date'], 'time': race['fp2_time']})
        if race.get('fp3_date') != r'\N' and race.get('fp3_time') != r'\N':
            sessions.append({'type': 'FP3', 'date': race['fp3_date'], 'time': race['fp3_time']})
        if race.get('sprint_date') != r'\N' and race.get('sprint_time') != r'\N':
            sessions.append({'type': 'Sprint', 'date': race['sprint_date'], 'time': race['sprint_time']})
        if race.get('quali_date') != r'\N' and race.get('quali_time') != r'\N':
            sessions.append({'type': 'Qualifying', 'date': race['quali_date'], 'time': race['quali_time']})
        if race.get('date') != r'\N' and race.get('time') != r'\N':
            sessions.append({'type': 'Race', 'date': race['date'], 'time': race['time']})
        
        race['sessions'] = sessions

    return races

def get_race_data(year, round):
    """
    Fetches data for a specific race round in a specified year.
    
    Args:
        year (int): The year of the season.
        round (int): The round number of the race.
    
    Returns:
        dict: A dictionary containing the race and circuit data along with additional circuit information.
    """
    race = Races.collection.find_one({'year': year, 'round': round}, {'_id': 0})
    if not race:
        return None

    circuit_id = race['circuitId']
    circuit = Circuits.collection.find_one({'circuitId': circuit_id}, {'_id': 0})
    if not circuit:
        return None

    # Get additional circuit information from CIRCUITS_INFO
    additional_info = CIRCUITS_INFO.get(circuit_id, {})

    if race['raceId'] in get_sprint_race_ids(year):
        sprint = 'true'
    else: sprint = 'false'

    return {
        'race': race,
        'circuit': circuit,
        'additional_info': additional_info,
        'sprint_weekend': sprint
    }

def generate_qualifying_table(race_id):
    """
    Generates the qualifying table for the specified race.
    
    Args:
        race_id (int): The ID of the race.
    
    Returns:
        list: A list of dictionaries containing the qualifying data.
    """
    results = list(Qualifying.collection.find({'raceId': race_id}, {'_id': 0}))
    qualifying_table = []

    for result in results:
        driver_id = result['driverId']
        constructor_id = result['constructorId']

        driver_name = get_driver_name(driver_id)
        team_name = get_team_name(constructor_id)

        qualifying_table.append({
            'position': result['position'],
            'team_color': TEAM_C[constructor_id],
            'driver_name': driver_name,
            'driver_pic': DRIVER_PIC[driver_id],
            'driver_nat_flag': NATIONALITY_FLAGS[driver_id],
            'team_name': team_name,
            'time': "No Time" if result['q1'] == "\\N" else (result['q3'] if result['q3'] != "\\N" else (result['q2'] if result['q2'] != "\\N" else result['q1']))
        })
    
    qualifying_table = sorted(qualifying_table, key=lambda x: x['position'])
    return qualifying_table

def generate_race_table(race_id):
    """
    Generates the race results table for the specified race.
    
    Args:
        race_id (int): The ID of the race.
    
    Returns:
        list: A list of dictionaries containing the race results data.
    """
    results = list(Results.collection.find({'raceId': race_id}, {'_id': 0}))
    race_table = []

    for result in results:
        driver_id = result['driverId']
        constructor_id = result['constructorId']

        driver_name = get_driver_name(driver_id)
        team_name = get_team_name(constructor_id)
        
        position_text = result['positionText']
        
        if result['time'] == "\\N":
            if position_text == "R":
                time_value = "DNF"
            elif position_text == "W":
                time_value = "DNS"
            else:
                status_id = result['statusId']
                status = Status.collection.find_one({'statusId': status_id}, {'status': 1, '_id': 0})
                time_value = status['status']
        else:
            time_value = result['time']

        fastest_lap = result['fastestLapTime'] if result['rank'] == 1 else ""

        race_table.append({
            'position': result['positionOrder'],
            'team_color': TEAM_C[constructor_id],
            'driver_name': driver_name,
            'driver_pic': DRIVER_PIC[driver_id],
            'driver_nat_flag': NATIONALITY_FLAGS[driver_id],
            'team_name': team_name,
            'time': time_value,
            'fastest_lap': fastest_lap
        })
    
    race_table = sorted(race_table, key=lambda x: x['position'])
    return race_table

def generate_sprint_table(race_id):
    """
    Generates the sprint race results table for the specified race.
    
    Args:
        race_id (int): The ID of the race.
    
    Returns:
        list: A list of dictionaries containing the sprint race results data.
    """
    results = list(SprintResults.collection.find({'raceId': race_id}, {'_id': 0}))
    sprint_table = []

    fastest_lap_time = None
    fastest_lap_driver = None

    for result in results:
        driver_id = result['driverId']
        constructor_id = result['constructorId']

        driver_name = get_driver_name(driver_id)
        team_name = get_team_name(constructor_id)
        
        position_text = result['positionText']
        
        if result['time'] == "\\N":
            if position_text == "R":
                time_value = "DNF"
            elif position_text == "W":
                time_value = "DNS"
            else:
                status_id = result['statusId']
                status = Status.collection.find_one({'statusId': status_id}, {'status': 1, '_id': 0})
                time_value = status['status']
        else:
            time_value = result['time']

        # Check for fastest lap
        if result['fastestLapTime'] != "\\N":
            lap_time = datetime.strptime(result['fastestLapTime'], '%M:%S.%f')
            if fastest_lap_time is None or lap_time < fastest_lap_time:
                fastest_lap_time = lap_time
                fastest_lap_driver = driver_id

        sprint_table.append({
            'position': result['positionOrder'],
            'team_color': TEAM_C[constructor_id],
            'driver_id': driver_id,
            'driver_name': driver_name,
            'driver_pic': DRIVER_PIC[driver_id],
            'driver_nat_flag': NATIONALITY_FLAGS[driver_id],
            'team_name': team_name,
            'time': time_value,
            'fastest_lap': ''  # Initialize as empty string
        })

    # Set fastest lap for the correct driver
    if fastest_lap_driver is not None:
        for result in sprint_table:
            if result['driver_id'] == fastest_lap_driver:
                result['fastest_lap'] = fastest_lap_time.strftime('%M:%S.%f')[:-3]

    sprint_table = sorted(sprint_table, key=lambda x: x['position'])
    return sprint_table
