from flask import Blueprint, jsonify
from services.history_service import generate_history_data

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def history():
    """
    Route to get historical data.
    
    Returns:
        response (json): A JSON response containing historical data.
    """
    history = generate_history_data()
    return jsonify(history), 200