from flask import Blueprint, jsonify

def team_bp(mongo):
    bp = Blueprint('team', __name__)

    @bp.route('/api/teams')
    def get_teams():
        teams = mongo.db.teams.find()
        return jsonify([team for team in teams])

    return bp