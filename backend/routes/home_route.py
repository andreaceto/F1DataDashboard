from flask import Blueprint, jsonify
from services.home_service import generate_home_data

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    """
    Home route that returns processed data for the homepage.
    
    Returns:
        response (json): A JSON response containing the processed data.
    """
    data = generate_home_data(2024)
    
    return jsonify(data)
