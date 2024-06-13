import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from services.common_service import TEAM_C, DRIVER_C, DRIVER_LS, LINESTYLES, get_dataframe
from data.model import *
import os

def get_championship_data(year):
    """
    Retrieves race and result data for the specified year, along with driver names.

    Args:
        year (int): The year for which to retrieve the data.

    Returns:
        tuple: A tuple containing a list of race results, a dictionary mapping race IDs to rounds,
               and a dictionary mapping driver IDs to driver names.
    """
    # Query to get race data for the specified year
    races = list(Races.collection.find({'year': year}, {'name': 1, 'raceId': 1, 'round': 1, '_id': 0}).sort('round'))
    # Extract race IDs from results
    race_ids = [race['raceId'] for race in races]

    # Query to get race results
    results = list(Results.collection.find({'raceId': {'$in': race_ids}}, {'raceId': 1, 'driverId': 1, 'position': 1, 'points': 1, '_id': 0}))
    sprint_results = list(SprintResults.collection.find({'raceId': {'$in': race_ids}}, {'raceId': 1, 'driverId': 1, 'position': 1, 'points': 1, '_id': 0}))
    results = results + sprint_results
    
    # Filter races to only include those that have results
    completed_race_ids = set(result['raceId'] for result in results)
    races = [race for race in races if race['raceId'] in completed_race_ids]
    
    # Extract driver IDs from results
    driver_ids = list(set(result['driverId'] for result in results))

    # Query to get driver names for the relevant driver IDs
    drivers = list(Drivers.collection.find({'driverId': {'$in': driver_ids}}, {'driverId': 1, 'forename': 1, 'surname': 1, '_id': 0}))

    return races, results, drivers

def generate_drivers_championship_plot(year):
    """
    Generates the drivers' championship plot for the specified year and saves it as an image.

    Returns:
        dict: A dictionary containing the relative path to the generated plot image.
    """
    races, results, drivers = get_championship_data(year)
    print(pd.DataFrame(races))
    print(pd.DataFrame(results))
    print(pd.DataFrame(drivers))

    # Create a map driver -> {race -> points}, summing points if there are multiple results for the same driver and race
    driver_points = defaultdict(lambda: defaultdict(int))
    for result in results:
        driver_id = result['driverId']
        race_id = result['raceId']
        points = result['points']
        driver_points[driver_id][race_id] += points
    
    # Create a dictionary mapping race IDs to GP names
    race_names = {race['raceId']: race['name'].replace("Grand Prix", "GP") for race in races}

    # Since the races are already sorted by round in the query, we can use them directly
    sorted_races = [race['raceId'] for race in races]

    # Calculate cumulative points for each driver
    driver_cumulative_points = {}
    for driver_id, race_points in driver_points.items():
        cumulative_points = [0]  # Start from 0
        total_points = 0
        for race_id in sorted_races:
            total_points += race_points.get(race_id, 0)
            cumulative_points.append(total_points)
        driver_cumulative_points[driver_id] = cumulative_points

    # Create a dictionary mapping driver IDs to driver names
    driver_names = {driver['driverId']: f"{driver['forename']} {driver['surname']}" for driver in drivers}

    # Sort drivers by their final cumulative points in descending order
    sorted_drivers = sorted(driver_cumulative_points.items(), key=lambda x: x[1][-1], reverse=True)

    # Generate the plot
    plt.rc("figure", figsize=(16, 12))
    plt.rc("font", size=(14))
    plt.rc("axes", xmargin=0.01)

    fig, ax = plt.subplots()
    for position, (driver_id, points) in enumerate(sorted_drivers, start=1):
        driver_name = driver_names.get(driver_id, f"Driver {driver_id}")
        ax.plot(range(len(points)), points, label=f"{position}. {driver_name}", color = DRIVER_C[driver_id], linestyle = LINESTYLES[DRIVER_LS[driver_id]])


    ax.set_xticks(range(len(sorted_races) + 1))  # +1 to account for the starting 0
    ax.set_xticklabels([''] + [f"{race_names[race_id]}" for race_id in sorted_races], rotation=45)
    ax.grid(axis="x", linestyle="--")
    ax.set_ylabel("Points")
    ax.set_title(f"F1 Drivers' World Championship — {year}")
    ax.legend()


    # Save the plot
    neutral_path = os.path.join('static', 'images', 'driver_championship_plot.png')
    storage_path = os.path.join(os.getcwd(), neutral_path)
    return_path = os.path.join('http://127.0.0.1:5000', neutral_path)
    fig.savefig(storage_path, format='png')
    plt.close(fig)

    return {'driver_championship_plot_path': return_path}

def generate_home_data():
    """
    Generates the home data including the driver championship plot path.

    Returns:
        dict: A dictionary containing the relative path to the generated plot image.
    """
    neutral_path = os.path.join('static', 'images', 'driver_championship_plot.png')
    storage_path = os.path.join(os.getcwd(), neutral_path)
    return_path = os.path.join('http://127.0.0.1:5000', neutral_path)

    if os.path.exists(storage_path):
        return {
            'driver_championship_plot_path': return_path
        }

    return generate_drivers_championship_plot(2024)