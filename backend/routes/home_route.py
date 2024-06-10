from flask import Blueprint, jsonify

# Define a blueprint for the home route
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    """
    Home route that returns a welcome message.
    
    Returns:
        response (json): A JSON response with a welcome message.
    """
    return jsonify({"message": "Welcome to F1 Data Dashboard!"})