from flask import Blueprint, jsonify, request
from data.model import RaceStats

# Define a blueprint for race statistics routes
race_stats_bp = Blueprint('race_stats', __name__)

@race_stats_bp.route('/raceStats', methods=['GET'])
def get_race_stats():
    """
    Route to get race statistics for a specific race.
    
    Query Parameters:
        race_id (str): The ID of the race.
    
    Returns:
        response (json): A JSON response containing race statistics or an error message.
    """
    race_id = request.args.get('race_id')
    if race_id:
        stats = RaceStats.find_one({"race_id": race_id})
        if stats:
            return jsonify(stats), 200
        return jsonify({"error": "Race not found"}), 404
    return jsonify({"error": "Race ID not provided"}), 400