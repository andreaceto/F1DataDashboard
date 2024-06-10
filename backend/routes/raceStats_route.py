from flask import Blueprint, jsonify, request
from services.raceStats_service import get_race_stats

race_stats_bp = Blueprint('race_stats', __name__)

@race_stats_bp.route('/raceStats', methods=['GET'])
def race_stats():
    """
    Route to get race statistics for a specific race.
    
    Query Parameters:
        race_id (str): The ID of the race.
    
    Returns:
        response (json): A JSON response containing race statistics or an error message.
    """
    race_id = request.args.get('race_id')
    if not race_id:
        return jsonify({"error": "Race ID not provided"}), 400

    stats = get_race_stats(race_id)
    if not stats:
        return jsonify({"error": "Race not found"}), 404

    return jsonify(stats), 200
