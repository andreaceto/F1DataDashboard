from flask import Blueprint, jsonify, request
from services.teamSection_service import get_teams, get_team

team_section_bp = Blueprint('team_section', __name__)

@team_section_bp.route('/teams', methods=['GET'])
def teams():
    """
    Route to get information about all teams.
    
    Returns:
        response (json): A JSON response containing information about all teams.
    """
    teams = get_teams()
    return jsonify(teams), 200

@team_section_bp.route('/teams/<team_id>', methods=['GET'])
def team(team_id):
    """
    Route to get information about a specific team.
    
    Args:
        team_id (str): The ID of the team.
    
    Returns:
        response (json): A JSON response containing information about the specified team or an error message.
    """
    team_info = get_team(team_id)
    if not team_info:
        return jsonify({"error": "Team not found"}), 404

    return jsonify(team_info), 200
