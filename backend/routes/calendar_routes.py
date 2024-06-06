from flask import Blueprint, jsonify

def calendar_bp(mongo):
    bp = Blueprint('calendar', __name__)

    @bp.route('/api/calendar')
    def get_calendar():
        calendar = mongo.db.calendar.find()
        return jsonify([event for event in calendar])

    return bp