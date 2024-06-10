from flask import Blueprint, jsonify
from services.home_service import generate_home_visualizations

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """
    Home route that returns visualizations for the homepage.
    
    Returns:
        response (json): A JSON response containing the visualizations.
    """
    visualizations = generate_home_visualizations()
    return jsonify(visualizations)
