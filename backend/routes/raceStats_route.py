from flask import Blueprint, jsonify, request
from services.raceStats_service import get_race_data, get_calendar

race_stats_bp = Blueprint('race_stats', __name__)

@race_stats_bp.route('/racestats/calendar/<int:year>', methods=['GET'])
def calendar(year):
    """
    Route to get the calendar for the specified season year.
    
    Args:
        year (int): The year of the season.

    Returns:
        response (json): A JSON response containing the race calendar.
    """
    data = get_calendar(year)
    return jsonify(data)

@race_stats_bp.route('/racestats/race/<int:year>/<int:round>', methods=['GET'])
def race_data(year, round):
    """
    Route to get data for a specific race round in a specified year.
    
    Args:
        year (int): The year of the season.
        round (int): The round number of the race.
    
    Returns:
        response (json): A JSON response containing the race data.
    """
    data = get_race_data(year, round)
    return jsonify(data)

