from flask import Blueprint, jsonify
from data.model import Calendar

# Define a blueprint for calendar routes
calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/calendar', methods=['GET'])
def get_calendar():
    """
    Route to get the race calendar.
    
    Returns:
        response (json): A JSON response containing the race calendar.
    """
    calendar = Calendar.find()
    return jsonify(list(calendar)), 200