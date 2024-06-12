from data.model import Races

def get_calendar():
    """
    Retrieves the race calendar.
    
    Returns:
        list: A list of races in the calendar.
    """
    return list(Races.find({}))