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

def get_driver_name(driver_id):
    """
    Retrieves the full name of the driver given the driver ID.

    Args:
        driver_id (int): The driver ID.

    Returns:
        str: Full name of the driver.
    """
    driver = Drivers.collection.find_one({'driverId': driver_id}, {'forename': 1, 'surname': 1, '_id': 0})
    if driver:
        return f"{driver['forename']} {driver['surname']}"
    return "Unknown Driver"

def get_team_name(constructor_id):
    """
    Retrieves the name of the team given the constructor ID.

    Args:
        constructor_id (int): The constructor ID.

    Returns:
        str: Name of the team.
    """
    team = Constructors.collection.find_one({'constructorId': constructor_id}, {'name': 1, '_id': 0})
    if team:
        return team['name']
    return "Unknown Team"

def get_sprint_race_ids(year):
    """
    Retrieves a list of race IDs that have a sprint race for the specified year.

    Args:
        year (int): The year for which to retrieve the race IDs.

    Returns:
        list: A list of race IDs with sprint races.
    """

    query = {
        'year': year,
        'sprint_date': {'$ne': '\\N'}
    }
    projection = {'raceId': 1, '_id': 0}

    races = list(Races.collection.find(query, projection))
    sprint_race_ids = [race['raceId'] for race in races]

    return sprint_race_ids

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

DRIVER_PIC = {
# DriverId : ProfilePic.png

                    # Red Bull
    830: "Verstappen.png", # Verstappen 
    815: "Perez.png", # Perez

                    # Mercedes
    1: "Hamilton.png", # Hamilton
    847: "Russell.png", # Russell

                    # Ferrari
    844: "Leclerc.png", # Leclerc
    832: "Sainz.png", # Sainz
    860: "Undefined.png", # Bearman

                    # McLaren
    846: "Norris.png", # Norris
    857: "Piastri.png", # Piastri

                    # Aston Martin
    4: "Alonso.png", # Alonso
    840: "Stroll.png", # Stroll

                    # Alpine
    842: "Gasly.png", # Gasly
    839: "Ocon.png", # Ocon

                    # Williams
    848: "Albon.png", # Albon
    858: "Sargeant.png", # Sargeant

                    # Racing Bulls
    852: "Tsunoda.png", # Tsunoda
    817: "Ricciardo.png", # Ricciardo

                    # Sauber
    822: "Bottas.png", # Bottas
    855: "Zhou.png", # Zhou

                    # Haas
    807: "Hulkenberg.png", # Hulkenberg
    825: "Magnussen.png", # Magnussen
}

NATIONALITY_FLAGS = {
# DriverId : Flag.png

                    # Red Bull
    830: "netherlands.png", # Verstappen 
    815: "mexico.png", # Perez

                    # Mercedes
    1: "uk.png", # Hamilton
    847: "uk.png", # Russell

                    # Ferrari
    844: "monaco.png", # Leclerc
    832: "spain.png", # Sainz
    860: "uk.png", # Bearman

                    # McLaren
    846: "uk.png", # Norris
    857: "australia.png", # Piastri

                    # Aston Martin
    4: "spain.png", # Alonso
    840: "canada.png", # Stroll

                    # Alpine
    842: "france.png", # Gasly
    839: "france.png", # Ocon

                    # Williams
    848: "thai.png", # Albon
    858: "usa.png", # Sargeant

                    # Racing Bulls
    852: "japan.png", # Tsunoda
    817: "australia.png", # Ricciardo

                    # Sauber
    822: "finland.png", # Bottas
    855: "china.png", # Zhou

                    # Haas
    807: "german.png", # Hulkenberg
    825: "denmark.png", # Magnussen
}

CIRCUITS_INFO = {
# CircuitId : Infos

    # Bahrain Grand Prix
    3: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Bahrain_Circuit',
        'first_gp': '2004',
        'laps': '57',
        'length': '5.412',
        'race_distance': '308.238',
        'lap_record': '1:31.447',
        'record_holder': 'P. de la Rosa (2005)'
    },
    # Saudi Arabian Grand Prix
    77: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Saudi_Arabia_Circuit',
        'first_gp': '2021',
        'laps': '50',
        'length': '6.174',
        'race_distance': '308.45',
        'lap_record': '1:30.734',
        'record_holder': 'L. Hamilton (2021)'
    },
    # Australian Grand Prix
    1: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_771/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Australia_Circuit',
        'first_gp': '1996',
        'laps': '58',
        'length': '5.278',
        'race_distance': '306.124',
        'lap_record': '1:19.813',
        'record_holder': 'C. Leclerc (2024)'
    },
    # Japanese Grand Prix
    22: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Japan_Circuit',
        'first_gp': '1987',
        'laps': '53',
        'length': '5.807',
        'race_distance': '307.471',
        'lap_record': '1:30.983',
        'record_holder': 'L. Hamilton (2019)'
    },
    # Chinese Grand Prix
    17: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/China_Circuit',
        'first_gp': '2004',
        'laps': '56',
        'length': '5.451',
        'race_distance': '305.066',
        'lap_record': '1:32.238',
        'record_holder': 'M. Schumacher (2004)'
    },
    # Miami Grand Prix
    79: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Miami_Circuit',
        'first_gp': '2022',
        'laps': '57',
        'length': '5.412',
        'race_distance': '308.326',
        'lap_record': '1:29.708',
        'record_holder': 'M. Verstappen (2023)'
    },
    # Emilia Romagna Grand Prix
    21: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Emilia_Romagna_Circuit',
        'first_gp': '1980',
        'laps': '63',
        'length': '4.909',
        'race_distance': '309.049',
        'lap_record': '1:15.484',
        'record_holder': 'L. Hamilton (2020)'
    },
    # Monaco Grand Prix
    6: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Monoco_Circuit',
        'first_gp': '1950',
        'laps': '78',
        'length': '3.337',
        'race_distance': '260.286',
        'lap_record': '1:12.909',
        'record_holder': 'L. Hamilton (2021)'
    },
    # Canadian Grand Prix
    7: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Canada_Circuit',
        'first_gp': '1978',
        'laps': '70',
        'length': '4.361',
        'race_distance': '305.27',
        'lap_record': '1:13.078',
        'record_holder': 'V. Bottas (2019)'
    },
    # Spanish Grand Prix
    4: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Spain_Circuit',
        'first_gp': '1991',
        'laps': '66',
        'length': '4.657',
        'race_distance': '307.236',
        'lap_record': '1:16.330',
        'record_holder': 'M. Verstappen (2023)'
    },
    # Austrian Grand Prix
    70: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Austria_Circuit',
        'first_gp': '1970',
        'laps': '71',
        'length': '4.318',
        'race_distance': '306.452',
        'lap_record': '1:05.619',
        'record_holder': 'C. Sainz (2020)'
    },
    # British Grand Prix
    9: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Great_Britain_Circuit',
        'first_gp': '1950',
        'laps': '52',
        'length': '5.891',
        'race_distance': '306.198',
        'lap_record': '1:27.097',
        'record_holder': 'M. Verstappen (2020)'
    },
    # Hungarian Grand Prix
    11: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Hungary_Circuit',
        'first_gp': '1986',
        'laps': '70',
        'length': '4.381',
        'race_distance': '306.63',
        'lap_record': '1:16.627',
        'record_holder': 'L. Hamilton (2020)'
    },
    # Belgian Grand Prix
    13: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Belgium_Circuit',
        'first_gp': '1950',
        'laps': '44',
        'length': '7.004',
        'race_distance': '308.052',
        'lap_record': '1:46.286',
        'record_holder': 'V. Bottas (2018)'
    },
    # Dutch Grand Prix
    39: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Netherlands_Circuit',
        'first_gp': '1952',
        'laps': '72',
        'length': '4.259',
        'race_distance': '306.587',
        'lap_record': '1:11.097',
        'record_holder': 'L. Hamilton (2021)'
    },
    # Italian Grand Prix
    14: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Italy_Circuit',
        'first_gp': '1950',
        'laps': '53',
        'length': '5.793',
        'race_distance': '306.72',
        'lap_record': '1:21.046',
        'record_holder': 'R. Barrichello (2004)'
    },
    # Azerbaijan Grand Prix
    73: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Baku_Circuit',
        'first_gp': '2016',
        'laps': '51',
        'length': '6.003',
        'race_distance': '306.049',
        'lap_record': '1:43.009',
        'record_holder': 'C. Leclerc (2019)'
    },
    # Singapore Grand Prix
    15: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Singapore_Circuit',
        'first_gp': '2008',
        'laps': '62',
        'length': '4.94',
        'race_distance': '306.143',
        'lap_record': '1:35.867',
        'record_holder': 'L. Hamilton (2023)'
    },
    # United States Grand Prix
    69: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/USA_Circuit',
        'first_gp': '2012',
        'laps': '56',
        'length': '5.513',
        'race_distance': '308.405',
        'lap_record': '1:36.169',
        'record_holder': 'C. Leclerc (2019)'
    },
    # Mexico City Grand Prix
    32: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Mexico_Circuit',
        'first_gp': '1963',
        'laps': '71',
        'length': '4.304',
        'race_distance': '305.354',
        'lap_record': '1:17.774',
        'record_holder': 'V. Bottas (2021)'
    },
    # São Paulo Grand Prix
    18: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Brazil_Circuit',
        'first_gp': '1973',
        'laps': '71',
        'length': '4.309',
        'race_distance': '305.879',
        'lap_record': '1:10.540',
        'record_holder': 'V. Bottas (2018)'
    },
    # Las Vegas Grand Prix
    80: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Las_Vegas_Circuit',
        'first_gp': '2023',
        'laps': '50',
        'length': '6.201',
        'race_distance': '309.958',
        'lap_record': '1:35.490',
        'record_holder': 'O. Piastri (2023)'
    },
    # Qatar Grand Prix
    78: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit maps 16x9/Qatar_Circuit',
        'first_gp': '2021',
        'laps': '57',
        'length': '5.419',
        'race_distance': '308.611',
        'lap_record': '1:24.319',
        'record_holder': 'M. Verstappen (2023)'
    },
    # Abu Dhabi Grand Prix
    24: {
        'img_src': 'https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Abu_Dhabi_Circuit',
        'first_gp': '2009',
        'laps': '58',
        'length': '5.281',
        'race_distance': '306.183',
        'lap_record': '1:26.103',
        'record_holder': 'M. Verstappen (2021)'
    },
}
