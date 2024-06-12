from data.model import Constructors, ConstructorResults

def get_teams():
    """
    Retrieves all teams.
    
    Returns:
        list: A list of all teams.
    """
    return list(Constructors.find({}))

def get_team(team_id):
    """
    Retrieves information for a specific team.
    
    Args:
        team_id (str): The ID of the team.
    
    Returns:
        dict: Team information or None if not found.
    """
    team = Constructors.find_one({"constructor_id": team_id})
    if not team:
        return None

    results = list(ConstructorResults.find({"constructor_id": team_id}))
    return {
        "team": team,
        "results": results
    }