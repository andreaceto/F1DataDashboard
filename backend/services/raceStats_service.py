from data.model import Results, Races

def get_race_stats(race_id):
    """
    Retrieves race statistics for a specific race.
    
    Args:
        race_id (str): The ID of the race.
    
    Returns:
        dict: Race statistics or None if not found.
    """
    race = Races.find_one({"race_id": race_id})
    if not race:
        return None

    results = list(Results.find({"race_id": race_id}))
    if not results:
        return None

    return {
        "race": race,
        "results": results
    }