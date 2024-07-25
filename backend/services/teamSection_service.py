from data.model import *
from services.common_service import *

from datetime import datetime

def get_teams(year):
    """
    Fetches teams with specific details from the Constructors collection.
    
    Returns:
        list: A list of dictionaries containing team details (constructorId, name, team_logo, and team_color).
    """
    races, results, sprint_results, drivers, teams = get_championship_data(year)
    
    # Filter and map the required details for each team
    filtered_teams = []
    for team in teams:
        constructor_id = team['constructorId']
        filtered_team = {
            'constructorId': constructor_id,
            'name': team['name'],
            'team_logo': TEAM_LOGOS.get(constructor_id, ''),
            'team_color': TEAM_C.get(constructor_id, '')
        }
        filtered_teams.append(filtered_team)
    
    return filtered_teams

def calculate_age(dob):
    """
    Calculates the age of a person given their date of birth.
    
    Args:
        dob (str): Date of birth in string format.
    
    Returns:
        int: Age in years.
    """
    if isinstance(dob, datetime):
        dob = dob.strftime('%a, %d %b %Y %H:%M:%S GMT')
    birth_date = datetime.strptime(dob, '%a, %d %b %Y %H:%M:%S GMT')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def format_dob(dob):
    """
    Formats the date of birth to 'Day Month Year'.
    
    Args:
        dob (str): Date of birth in string format.
    
    Returns:
        str: Formatted date of birth.
    """
    if isinstance(dob, datetime):
        dob = dob.strftime('%a, %d %b %Y %H:%M:%S GMT')
    birth_date = datetime.strptime(dob, '%a, %d %b %Y %H:%M:%S GMT')
    return birth_date.strftime('%d %b %Y')

def get_team_stats(team_id, year):
    """
    Fetches statistics for a specific team and its drivers for a given year.

    Args:
        team_id (str): The ID of the team.
        year (int): The year for which to retrieve the data.

    Returns:
        dict: A dictionary containing team and driver statistics.
    """
    # Team ID parsing
    team_id = int(team_id)

    # Get championship data for the specified year
    races, results, sprint_results, drivers, constructors = get_championship_data(year)

    # Combine race results and sprint results
    combined_results = results + sprint_results
    
    # Generate the team-driver map
    team_driver_map = generate_team_driver_map(combined_results)

    # Get the team details
    team = next((constructor for constructor in constructors if constructor['constructorId'] == team_id), None)

    # Get the driver IDs for the specified team
    driver_ids = team_driver_map.get(team_id, [])

    # I don't want third drivers to show
    if 860 in driver_ids: driver_ids.remove(860)
    
    # Filter the drivers to get the details of the team's drivers
    team_drivers = [driver for driver in drivers if driver['driverId'] in driver_ids]
    
    # Aggregate driver stats
    driver_stats = []
    team_points = 0
    team_wins = 0
    team_podiums = 0
    team_sprint_wins = 0
    team_sprint_podiums = 0
    team_poles = 0
    team_sprint_poles = 0

    for driver in team_drivers:
        driver_id = driver['driverId']

        results = [result for result in combined_results if result['driverId'] == driver_id]

        points = sum(result['points'] for result in results)
        wins = sum(1 for result in results if result['positionOrder'] == 1)
        sprint_wins = sum(1 for result in sprint_results if result['driverId'] == driver_id and result['positionOrder'] == 1)
        podiums = sum(1 for result in results if result['positionOrder'] <= 3)
        sprint_podiums = sum(1 for result in sprint_results if result['driverId'] == driver_id and result['positionOrder'] <= 3)
        poles = sum(1 for result in results if result['grid'] == 1)
        sprint_poles = sum(1 for result in sprint_results if result['driverId'] == driver_id and result['grid'] == 1)

        # Calculate formatted date of birth and age
        formatted_dob = format_dob(driver['dob'])
        age = calculate_age(driver['dob'])

        driver_stats.append({
            'driverId': driver_id,
            'driver_pic': DRIVER_PIC.get(driver_id, ''),
            'forename': driver['forename'],
            'surname': str(driver['surname']).upper(),
            'number': driver['number'],
            'nat_flag': NATIONALITY_FLAGS.get(driver_id, ''),
            'dob': formatted_dob,
            'age': age,
            'points': points,
            'wins': wins - sprint_wins,
            'sprint_wins': sprint_wins,
            'podiums': podiums - sprint_podiums,
            'sprint_podiums': sprint_podiums,
            'poles': poles - sprint_poles,
            'sprint_poles': sprint_poles
        })

        # Aggregate team stats
        team_points += points
        team_wins += wins
        team_podiums += podiums
        team_sprint_wins += sprint_wins
        team_sprint_podiums += sprint_podiums
        team_poles += poles
        team_sprint_poles += sprint_poles

    team_stats = {
        'constructorId': team_id,
        'name': team['name'],
        'team_nat_flag': TEAM_NAT_FLAGS.get(team_id, ''),
        'team_logo': TEAM_LOGOS.get(team_id, ''),
        'team_color': TEAM_C.get(team_id, ''),
        'team_car': CARS.get(team_id, '')[0],
        'car_name': CARS.get(team_id, '')[1],
        'points': team_points,
        'wins': team_wins - team_sprint_wins,
        'podiums': team_podiums - team_sprint_podiums,
        'sprint_wins': team_sprint_wins,
        'sprint_podiums': team_sprint_podiums,
        'poles': team_poles - team_sprint_poles,
        'sprint_poles': team_sprint_poles
    }

    return {'team': team_stats, 'drivers': driver_stats}
