from data.model import Races, Circuits
from services.common_service import CIRCUITS_INFO

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

    return {
        'race': race,
        'circuit': circuit,
        'additional_info': additional_info
    }
