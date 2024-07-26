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
    races, results, sprint_results, drivers, constructors = get_championship_data(year)
    
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
        ax.plot(range(len(points)), points, label=f"{position}. {driver_name}", color=DRIVER_C[driver_id], linestyle=LINESTYLES[DRIVER_LS[driver_id]])

    ax.set_xticks(range(len(sorted_races) + 1))  # +1 to account for the starting 0
    ax.set_xticklabels([''] + [f"{race_names[race_id]}" for race_id in sorted_races], rotation=30, fontweight='bold', color='white')
    ax.grid(axis="x", linestyle="--")
    ax.set_ylabel("Points", fontweight='bold', color='white')
    ax.set_title(f"F1 Drivers' World Championship — {year}", fontweight='bold', color='white')
    ax.legend()

    # Make the background transparent
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Set white and bold labels for y-ticks
    plt.yticks(color='white', fontweight='bold')
    plt.xticks(color='white', fontweight='bold')

    # Set white and bold labels for legend
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_fontweight("bold")

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
    
    # Initialize dictionary to store driver standings data
    driver_standings = defaultdict(lambda: {
        'Name': '',
        'Surname': '',
        'TeamC': '',
        'ProPic': '',
        'NatFlag': '',
        'TeamLogo': '',
        'Points': 0,
        'Poles': 0,
        'SprintPoles': 0,
        'Wins': 0,
        'SprintWins': 0,
        'Podiums': 0,
        'SprintPodiums': 0,
        'FastestLaps': 0
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
        if result['grid'] == 1:
            driver_standings[driver_id]['Poles'] += 1
        if result['rank'] == 1:
            driver_standings[driver_id]['FastestLaps'] += 1

        driver_standings[driver_id]['TeamC'] = TEAM_C.get(constructor_id, '')
        driver_standings[driver_id]['TeamLogo'] = TEAM_LOGOS.get(constructor_id, '')

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
        if sprint_result['grid'] == 1:
            driver_standings[driver_id]['SprintPoles'] += 1

    # Fill in driver and team information
    for driver_id, info in driver_info.items():
        driver_standings[driver_id]['Name'] = info['forename']
        driver_standings[driver_id]['Surname'] = str(info['surname']).upper()
        driver_standings[driver_id]['ProPic'] = DRIVER_PIC.get(driver_id, '')
        driver_standings[driver_id]['NatFlag'] = NATIONALITY_FLAGS.get(driver_id, '')


    # Sort drivers by their final cumulative points in descending order, then by positionOrder
    driver_final_positions = {result['driverId']: result['positionOrder'] for result in results + sprint_results}
    sorted_standings = sorted(driver_standings.items(), key=lambda x: (x[1]['Points'], -driver_final_positions.get(x[0], float('inf'))), reverse=True)

    # Create a DataFrame for better formatting
    df_standings = pd.DataFrame([standings for driver_id, standings in sorted_standings])
    df_standings.index = range(1, len(df_standings) + 1)
    df_standings.reset_index(inplace=True)
    df_standings.rename(columns={'index': 'Position'}, inplace=True)

    return df_standings.to_dict(orient='records')

def generate_constructors_championship_plot(year):
    """
    Generates the constructors' championship plot for the specified year and saves it as an image.

    Returns:
        dict: A dictionary containing the relative path to the generated plot image.
    """
    races, results, sprint_results, drivers, constructors = get_championship_data(year)
    
    # Combine results and sprint results
    combined_results = results + sprint_results
    
    # Create a map constructor -> {race -> points}
    constructor_points = defaultdict(lambda: defaultdict(int))
    for result in combined_results:
        constructor_id = result['constructorId']
        race_id = result['raceId']
        points = result['points']
        constructor_points[constructor_id][race_id] += points
    
    # Create a dictionary mapping race IDs to GP names
    race_names = {race['raceId']: race['name'].replace("Grand Prix", "GP") for race in races}
    sorted_races = [race['raceId'] for race in races]

    # Calculate cumulative points for each constructor
    constructor_cumulative_points = {}
    for constructor_id, race_points in constructor_points.items():
        cumulative_points = [0]  # Start from 0
        total_points = 0
        for race_id in sorted_races:
            total_points += race_points.get(race_id, 0)
            cumulative_points.append(total_points)
        constructor_cumulative_points[constructor_id] = cumulative_points

    # Create a dictionary mapping constructor IDs to constructor names
    constructor_names = {constructor['constructorId']: constructor['name'] for constructor in constructors}

    # Sort constructors by their final cumulative points in descending order
    sorted_constructors = sorted(constructor_cumulative_points.items(), key=lambda x: x[1][-1], reverse=True)

    # Generate the plot
    plt.rc("figure", figsize=(16, 12))
    plt.rc("font", size=(14))
    plt.rc("axes", xmargin=0.01)

    fig, ax = plt.subplots()
    for position, (constructor_id, points) in enumerate(sorted_constructors, start=1):
        constructor_name = constructor_names.get(constructor_id, f"Constructor {constructor_id}")
        ax.plot(range(len(points)), points, label=f"{position}. {constructor_name}", color=TEAM_C[constructor_id], linestyle='-')

    ax.set_xticks(range(len(sorted_races) + 1))  # +1 to account for the starting 0
    ax.set_xticklabels([''] + [f"{race_names[race_id]}" for race_id in sorted_races], rotation=30, fontweight='bold', color='white')
    ax.grid(axis="x", linestyle="--")
    ax.set_ylabel("Points", fontweight='bold', color='white')
    ax.set_title(f"F1 Constructors' World Championship — {year}", fontweight='bold', color='white')
    ax.legend()

    # Make the background transparent
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    # Set white and bold labels for y-ticks
    plt.yticks(color='white', fontweight='bold')
    plt.xticks(color='white', fontweight='bold')

    # Set white and bold labels for legend
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_fontweight("bold")

    # Save the plot
    neutral_path = os.path.join('static', 'images', 'constructor_championship_plot.png')
    storage_path = os.path.join(os.getcwd(), neutral_path)
    return_path = os.path.join('http://127.0.0.1:5000', neutral_path)
    fig.savefig(storage_path, format='png', transparent=True)
    plt.close(fig)

    return {'constructor_championship_plot_path': return_path}

def generate_constructors_standings_table(year):
    """
    Generates the constructors' standings table for the specified year.

    Returns:
        dict: A dictionary containing the constructors' standings table data.
    """
    races, results, sprint_results, drivers, constructors = get_championship_data(year)

    # Create a map constructor_id -> constructor_info
    constructor_info = {constructor['constructorId']: constructor for constructor in constructors}
    
    # Create a map driver_id -> driver_surname
    driver_surnames = {driver['driverId']: driver['surname'] for driver in drivers}

    # Initialize dictionary to store constructor standings data
    constructor_standings = defaultdict(lambda: {
        'TeamC': '',
        'Car': '',
        'Constructor': '',
        'Drivers': [],
        'Points': 0,
        'Poles': 0,
        'SprintPoles': 0,
        'Wins': 0,
        'Podiums': 0,
        'SprintWins': 0,
        'SprintPodiums': 0,
        'FastestLaps': 0
    })
    
    # Process each result to update constructor standings
    for result in results:
        constructor_id = result['constructorId']
        points = result['points']
        position = result['positionOrder']
        driver_id = result['driverId']
        
        constructor_standings[constructor_id]['Points'] += points
        if position == 1:
            constructor_standings[constructor_id]['Wins'] += 1
        if position <= 3:
            constructor_standings[constructor_id]['Podiums'] += 1
        if result['grid'] == 1:
             constructor_standings[constructor_id]['Poles'] += 1
        if result['rank'] == 1:
             constructor_standings[constructor_id]['FastestLaps'] += 1
        constructor_standings[constructor_id]['Drivers'].append(driver_surnames[driver_id])

    # Process each sprint result to update constructor standings
    for sprint_result in sprint_results:
        constructor_id = sprint_result['constructorId']
        points = sprint_result['points']
        position = sprint_result['positionOrder']
        driver_id = sprint_result['driverId']
        
        constructor_standings[constructor_id]['Points'] += points
        if position == 1:
            constructor_standings[constructor_id]['SprintWins'] += 1
        if position <= 3:
            constructor_standings[constructor_id]['SprintPodiums'] += 1
        if sprint_result['grid'] == 1:
             constructor_standings[constructor_id]['SprintPoles'] += 1
        constructor_standings[constructor_id]['Drivers'].append(driver_surnames[driver_id])

    # Fill in constructor information
    for constructor_id, info in constructor_info.items():
        constructor_standings[constructor_id]['Constructor'] = info['name']
        constructor_standings[constructor_id]['TeamC'] = TEAM_C.get(constructor_id, '')
        constructor_standings[constructor_id]['Car'] = CARS.get(constructor_id, '')[0]

    # Remove duplicates from drivers list
    for constructor_id in constructor_standings:
        constructor_standings[constructor_id]['Drivers'] = list(set(constructor_standings[constructor_id]['Drivers']))

    # Sort constructors by their final cumulative points in descending order
    sorted_standings = sorted(constructor_standings.items(), key=lambda x: x[1]['Points'], reverse=True)

    # Create a DataFrame for better formatting
    df_standings = pd.DataFrame([standings for constructor_id, standings in sorted_standings])
    df_standings.index = range(1, len(df_standings) + 1)
    df_standings.reset_index(inplace=True)
    df_standings.rename(columns={'index': 'Position'}, inplace=True)

    return df_standings.to_dict(orient='records')

def generate_home_data(year):
    """
    Generates the home data including the driver and constructor championship plot paths and standings tables.

    Returns:
        dict: A dictionary containing the relative paths to the generated plot images and standings tables.
    """
    ## DRIVER STANDINGS PLOT&TABLE ##
    neutral_path = os.path.join('static', 'images', 'driver_championship_plot.png')
    storage_path = os.path.join(os.getcwd(), neutral_path)
    return_path = os.path.join('http://127.0.0.1:5000', neutral_path)

    if os.path.exists(storage_path):
        driver_plot_path = return_path
    else:
        driver_plot_path = generate_drivers_championship_plot(year)['driver_championship_plot_path']
    driver_standings_table = generate_drivers_standings_table(year)

    ## CONSTRUCTOR STANDINGS PLOT&TABLE ##
    neutral_path = os.path.join('static', 'images', 'constructor_championship_plot.png')
    storage_path = os.path.join(os.getcwd(), neutral_path)
    return_path = os.path.join('http://127.0.0.1:5000', neutral_path)

    if os.path.exists(storage_path):
        constructor_plot_path = return_path
    else:
        constructor_plot_path = generate_constructors_championship_plot(year)['constructor_championship_plot_path']
    constructor_standings_table = generate_constructors_standings_table(year)

    return {
        'driver_championship_plot_path': driver_plot_path,
        'driver_standings_table': driver_standings_table,
        'constructor_championship_plot_path': constructor_plot_path,
        'constructor_standings_table': constructor_standings_table
    }