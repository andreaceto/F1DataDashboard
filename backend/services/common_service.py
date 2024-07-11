from collections import defaultdict

from data.model import *

def get_championship_data(year):
    """
    Retrieves race, result, sprint result, driver, and team data for the specified year.

    Args:
        year (int): The year for which to retrieve the data.

    Returns:
        tuple: A tuple containing the following elements:
            - races (list): A list of race documents from the 'races' collection, including 'raceId', 'round', and 'name'.
            - results (list): A list of result documents from the 'results' collection, including 'raceId', 'driverId', 'positionOrder', 'points', and 'constructorId'.
            - sprint_results (list): A list of sprint result documents from the 'sprint_results' collection, including 'raceId', 'driverId', 'positionOrder', 'points', and 'constructorId'.
            - drivers (list): A list of driver documents from the 'drivers' collection, including 'driverId', 'forename', 'surname', and 'nationality'.
            - constructors (list): A list of constructor documents from the 'constructors' collection, including 'constructorId' and 'name'.
    """
    # Query to get race data for the specified year
    races = list(Races.collection.find({'year': year}, {'name': 1, 'raceId': 1, 'round': 1, '_id': 0}).sort('round'))
    # Extract race IDs from results
    race_ids = [race['raceId'] for race in races]

    # Query to get race results
    results = list(Results.collection.find({'raceId': {'$in': race_ids}}, {'raceId': 1, 'driverId': 1, 'positionOrder': 1, 'points': 1, 'constructorId': 1, '_id': 0}))
    sprint_results = list(SprintResults.collection.find({'raceId': {'$in': race_ids}}, {'raceId': 1, 'driverId': 1, 'positionOrder': 1, 'points': 1, 'constructorId': 1, '_id': 0}))
    combined_results = results + sprint_results
    
    # Filter races to only include those that have results
    completed_race_ids = set(result['raceId'] for result in combined_results)
    races = [race for race in races if race['raceId'] in completed_race_ids]
    
    # Extract driver IDs from results
    driver_ids = list(set(result['driverId'] for result in combined_results))
    # Query to get driver names for the relevant driver IDs
    drivers = list(Drivers.collection.find({'driverId': {'$in': driver_ids}}, {'driverId': 1, 'forename': 1, 'surname': 1, 'nationality': 1, '_id': 0}))

    # Extract team IDs from combined results
    constructor_ids = list(set(result['constructorId'] for result in combined_results))
    # Query to get team names for the relevant team IDs
    constructors = list(Constructors.collection.find({'constructorId': {'$in': constructor_ids}}, {'constructorId': 1, 'name': 1, 'nationality':1, '_id': 0}))
    
    return races, results, sprint_results, drivers, constructors

def generate_team_driver_map(results):
    """
    Generates a dictionary mapping constructorId to a list of driverIds from the results.

    Args:
        results (list): A list of result documents, each containing 'constructorId' and 'driverId'.

    Returns:
        dict: A dictionary where keys are constructorIds and values are lists of driverIds.
    """
    team_driver_map = defaultdict(list)
    
    for result in results:
        constructor_id = result['constructorId']
        driver_id = result['driverId']
        if driver_id not in team_driver_map[constructor_id]:
            team_driver_map[constructor_id].append(driver_id)
    
    return dict(team_driver_map)

TEAM_C = {
# ConstructorId : Color Hex Code
    9: "#3671C6", # Red Bull
    131: "#27F4D2", # Mercedes
    6: "#E8002D", # Ferrari
    1: "#FF8000", # McLaren
    117: "#229971", # Aston Martin
    214: "#FF87BC", # Alpine
    3: "#64C4FF", # Williams
    215: "#6692FF", # Racing Bulls
    15: "#52E252", # Sauber
    210: "#B6BABD"  # Haas
}

DRIVER_C = {
# DriverId : Color Hex Code
                  # Red Bull
    830: "#3671C6", # Verstappen 
    815: "#3671C6", # Perez

                  # Mercedes
    1: "#27F4D2", # Hamilton
    847: "#27F4D2", # Russell

                  # Ferrari
    844: "#E8002D", # Leclerc
    832: "#E8002D", # Sainz
    860: "#E8002D", # Bearman

                  # McLaren
    846: "#FF8000", # Norris
    857: "#FF8000", # Piastri

                  # Aston Martin
    4: "#229971", # Alonso
    840: "#229971", # Stroll

                  # Alpine
    842: "#FF87BC", # Gasly
    839: "#FF87BC", # Ocon

                  # Williams
    848: "#64C4FF", # Albon
    858: "#64C4FF", # Sargeant

                  # Racing Bulls
    852: "#6692FF", # Tsunoda
    817: "#6692FF", # Ricciardo

                  # Sauber
    822: "#52E252", # Bottas
    855: "#52E252", # Zhou

                  # Haas
    807: "#B6BABD", # Hulkenberg
    825: "#B6BABD"  # Magnussen
}

DRIVER_LS= {
# DriverId : Line Style
                  # Red Bull
    830: "solid", # Verstappen 
    815: "dashdot", # Perez

                  # Mercedes
    1: "solid", # Hamilton
    847: "dashdot", # Russell

                  # Ferrari
    844: "solid", # Leclerc
    832: "dashdot", # Sainz
    860: "dashed", # Bearman

                  # McLaren
    846: "solid", # Norris
    857: "dashdot", # Piastri

                  # Aston Martin
    4: "solid", # Alonso
    840: "dashdot", # Stroll

                  # Alpine
    842: "solid", # Gasly
    839: "dashdot", # Ocon

                  # Williams
    848: "solid", # Albon
    858: "dashdot", # Sargeant

                  # Racing Bulls
    852: "solid", # Tsunoda
    817: "dashdot", # Ricciardo

                  # Sauber
    822: "solid", # Bottas
    855: "dashdot", # Zhou

                  # Haas
    807: "solid", # Hulkenberg
    825: "dashdot", # Magnussen
}

LINESTYLES = {
    "solid": '-',
    "dashdot": '-.',
    "dashed": '--'
}
