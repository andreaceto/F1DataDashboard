from flask import Blueprint, jsonify
from services.calendar_service import get_calendar

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar', methods=['GET'])
def calendar():
    """
    Route to get the race calendar.
    
    Returns:
        response (json): A JSON response containing the race calendar.
    """
    calendar = get_calendar()
    return jsonify(calendar), 200
