from flask import Blueprint, jsonify, request
from services.raceStats_service import *

race_stats_bp = Blueprint('race_stats', __name__)

@race_stats_bp.route('/racestats/calendar/<int:year>', methods=['GET'])
def fetch_calendar(year):
    try:
        calendar = get_calendar(year)
        return jsonify(calendar)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@race_stats_bp.route('/racestats/race/<int:year>/<int:round>', methods=['GET'])
def fetch_race_data(year, round):
    try:
        race_data = get_race_data(year, round)
        return jsonify(race_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@race_stats_bp.route('/racestats/qualifying/<int:race_id>', methods=['GET'])
def fetch_qualifying_table(race_id):
    try:
        qualifying_table = generate_qualifying_table(race_id)
        return jsonify(qualifying_table)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@race_stats_bp.route('/racestats/race/<int:race_id>', methods=['GET'])
def fetch_race_table(race_id):
    try:
        race_table = generate_race_table(race_id)
        return jsonify(race_table)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@race_stats_bp.route('/racestats/sprint/<int:race_id>', methods=['GET'])
def fetch_sprint_table(race_id):
    try:
        sprint_table = generate_sprint_table(race_id)
        return jsonify(sprint_table)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

