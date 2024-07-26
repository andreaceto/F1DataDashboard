from flask import Blueprint, jsonify, request
from flask import Blueprint, jsonify
from services.teamSection_service import get_teams, get_team_stats

team_section_bp = Blueprint('teams', __name__)

@team_section_bp.route('/teams', methods=['GET'])
def teams():
    """
    Endpoint to get all teams.

    Returns:
        Response: JSON response containing the list of teams.
    """
    teams = get_teams(2024)
    return jsonify(teams)

@team_section_bp.route('/teams/<team_id>', methods=['GET'])
def team_stats(team_id):
    """
    Endpoint to get statistics for a specific team.

    Args:
        team_id (str): The ID of the team.

    Returns:
        Response: JSON response containing team and driver statistics.
    """
    stats = get_team_stats(team_id, 2024)
    return jsonify(stats)

