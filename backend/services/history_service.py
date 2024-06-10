from data.model import Seasons, DriverStandings, ConstructorStandings

def get_history():
    """
    Retrieves historical data.
    
    Returns:
        dict: A dictionary containing historical data.
    """
    seasons = list(Seasons.find({}))
    driver_standings = list(DriverStandings.find({}))
    constructor_standings = list(ConstructorStandings.find({}))

    return {
        "seasons": seasons,
        "driver_standings": driver_standings,
        "constructor_standings": constructor_standings
    }