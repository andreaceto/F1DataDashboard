from flask import Blueprint, jsonify, request
from data.model import Team

# Define a blueprint for team section routes
team_section_bp = Blueprint('team_section', __name__)

@team_section_bp.route('/teams', methods=['GET'])
def get_teams():
    """
    Route to get information about all teams.
    
    Returns:
        response (json): A JSON response containing information about all teams.
    """
    teams = Team.find()
    return jsonify(list(teams)), 200

@team_section_bp.route('/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    """
    Route to get information about a specific team.
    
    Args:
        team_id (str): The ID of the team.
    
    Returns:
        response (json): A JSON response containing information about the specified team or an error message.
    """
    team = Team.find_one({"team_id": team_id})
    if team:
        return jsonify(team), 200
    return jsonify({"error": "Team not found"}), 404