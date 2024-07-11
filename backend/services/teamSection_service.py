from data.model import *
from services.common_service import *

def get_teams(year):
    """
    Fetches all teams from the Constructors collection.
    
    Returns:
        list: A list of all teams.
    """
    races, results, sprint_results, drivers, teams = get_championship_data(year)
    
    return teams

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
    
    # Filter the drivers to get the details of the team's drivers
    team_drivers = [driver for driver in drivers if driver['driverId'] in driver_ids]
    
    # Aggregate driver stats
    driver_stats = []
    team_points = 0
    team_wins = 0
    team_podiums = 0
    team_sprint_wins = 0
    team_sprint_podiums = 0

    for driver in team_drivers:
        driver_id = driver['driverId']
        results = [result for result in combined_results if result['driverId'] == driver_id]
        
        points = sum(result['points'] for result in results)
        wins = sum(1 for result in results if result['positionOrder'] == 1)
        sprint_wins = sum(1 for result in sprint_results if result['driverId'] == driver_id and result['positionOrder'] == 1)
        podiums = sum(1 for result in results if result['positionOrder'] <= 3)
        sprint_podiums = sum(1 for result in sprint_results if result['driverId'] == driver_id and result['positionOrder'] <= 3)

        driver_stats.append({
            'driverId': driver_id,
            'forename': driver['forename'],
            'surname': driver['surname'],
            'nationality': driver['nationality'],
            'points': points,
            'wins': wins,
            'sprint_wins': sprint_wins,
            'podiums': podiums,
            'sprint_podiums': sprint_podiums
        })

        # Aggregate team stats
        team_points += points
        team_wins += wins
        team_podiums += podiums
        team_sprint_wins += sprint_wins
        team_sprint_podiums += sprint_podiums

    team_stats = {
        'constructorId': team_id,
        'name': team['name'],
        'points': team_points,
        'wins': team_wins,
        'podiums': team_podiums,
        'sprint_wins': team_sprint_wins,
        'sprint_podiums': team_sprint_podiums
    }

    return {'team': team_stats, 'drivers': driver_stats}
