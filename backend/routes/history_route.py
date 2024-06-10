from flask import Blueprint, jsonify
from data.model import History

# Define a blueprint for history routes
history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def get_history():
    """
    Route to get historical data.
    
    Returns:
        response (json): A JSON response containing historical data.
    """
    history = History.find()
    return jsonify(list(history)), 200