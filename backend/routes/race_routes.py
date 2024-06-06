from flask import Blueprint, jsonify

def race_bp(mongo):
    bp = Blueprint('race', __name__)

    @bp.route('/api/races')
    def get_races():
        races = mongo.db.races.find()
        return jsonify([race for race in races])

    return bp