import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
from services.common_service import *
from data.model import *
import os

def generate_drivers_championship_plot(year):
    """
    Generates the drivers' championship plot for the specified year and saves it as an image.

    Returns:
        dict: A dictionary containing the relative path to the generated plot image.
    """
    races, results, sprint_results, drivers, constructos = get_championship_data(year)
    
    # Combining results makes no differences 
    results = results + sprint_results
    
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

    # Sort drivers by their final cumulative points in descending order, then by positionOrder
    driver_final_positions = {result['driverId']: result['positionOrder'] for result in results}
    sorted_drivers = sorted(driver_cumulative_points.items(), key=lambda x: (x[1][-1], -driver_final_positions.get(x[0], float('inf'))), reverse=True)

    # Generate the plot
    plt.rc("figure", figsize=(16, 12))
    plt.rc("font", size=(14))
    plt.rc("axes", xmargin=0.01)

    fig, ax = plt.subplots()
    for position, (driver_id, points) in enumerate(sorted_drivers, start=1):
        driver_name = driver_names.get(driver_id, f"Driver {driver_id}")
        ax.plot(range(len(points)), points, label=f"{position}. {driver_name}", color = DRIVER_C[driver_id], linestyle = LINESTYLES[DRIVER_LS[driver_id]])


    ax.set_xticks(range(len(sorted_races) + 1))  # +1 to account for the starting 0
    ax.set_xticklabels([''] + [f"{race_names[race_id]}" for race_id in sorted_races], rotation=30)
    ax.grid(axis="x", linestyle="--")
    ax.set_ylabel("Points")
    ax.set_title(f"F1 Drivers' World Championship — {year}")
    ax.legend()

    # Make the background transparent
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Save the plot
    neutral_path = os.path.join('static', 'images', 'driver_championship_plot.png')
    storage_path = os.path.join(os.getcwd(), neutral_path)
    return_path = os.path.join('http://127.0.0.1:5000', neutral_path)
    fig.savefig(storage_path, format='png', transparent=True)
    plt.close(fig)

    return {'driver_championship_plot_path': return_path}

def generate_drivers_standings_table(year):
    """
    Generates the drivers' standings table for the specified year.

    Returns:
        dict: A dictionary containing the drivers' standings table data.
    """
    races, results, sprint_results, drivers, constructors = get_championship_data(year)

    # Create a map driver_id -> driver_info
    driver_info = {driver['driverId']: driver for driver in drivers}

    # Create a map constructor_id -> constructor_name
    constructor_info = {constructor['constructorId']: constructor['name'] for constructor in constructors}
    
    # Initialize dictionary to store driver standings data
    driver_standings = defaultdict(lambda: {
        'Driver': '',
        'Nationality': '',
        'Team': '',
        'Points': 0,
        'Wins': 0,
        'SprintWins': 0,
        'Podiums': 0,
        'SprintPodiums': 0
    })
    
    # Process each result to update driver standings
    for result in results:
        driver_id = result['driverId']
        points = result['points']
        position = result['positionOrder']
        constructor_id = result['constructorId']
        
        driver_standings[driver_id]['Points'] += points
        if position == 1:
            driver_standings[driver_id]['Wins'] += 1
        if position <= 3:
            driver_standings[driver_id]['Podiums'] += 1
        driver_standings[driver_id]['Team'] = constructor_info.get(constructor_id, 'Unknown')

    # Process each sprint result to update driver standings
    for sprint_result in sprint_results:
        driver_id = sprint_result['driverId']
        points = sprint_result['points']
        position = sprint_result['positionOrder']
        
        driver_standings[driver_id]['Points'] += points
        if position == 1:
            driver_standings[driver_id]['SprintWins'] += 1
        if position <= 3:
            driver_standings[driver_id]['SprintPodiums'] += 1

    # Fill in driver and team information
    for driver_id, info in driver_info.items():
        driver_standings[driver_id]['Driver'] = f"{info['forename']} {info['surname']}"
        driver_standings[driver_id]['Nationality'] = info['nationality']

    # Sort drivers by their final cumulative points in descending order, then by positionOrder
    driver_final_positions = {result['driverId']: result['positionOrder'] for result in results + sprint_results}
    sorted_standings = sorted(driver_standings.items(), key=lambda x: (x[1]['Points'], -driver_final_positions.get(x[0], float('inf'))), reverse=True)

    # Create a DataFrame for better formatting
    df_standings = pd.DataFrame([standings for driver_id, standings in sorted_standings])
    df_standings.index = range(1, len(df_standings) + 1)
    df_standings.reset_index(inplace=True)
    df_standings.rename(columns={'index': 'Position'}, inplace=True)

    return df_standings.to_dict(orient='records')

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
        plot_path = return_path
    else:
        plot_path = generate_drivers_championship_plot(2024)
    
    standings_table = generate_drivers_standings_table(2024)

    return {
        'driver_championship_plot_path': plot_path,
        'drivers_standings_table': standings_table
    }