from flask import Flask
from flask_cors import CORS
from routes import home_route, raceStats_route, teamSection_route, calendar_route, history_route

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        app (Flask): The configured Flask application.
    """
    app = Flask(__name__, static_folder='static')

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Register blueprints for different routes
    app.register_blueprint(home_route.home_bp)
    app.register_blueprint(raceStats_route.race_stats_bp)
    app.register_blueprint(teamSection_route.team_section_bp)
    app.register_blueprint(calendar_route.calendar_bp)
    app.register_blueprint(history_route.history_bp)

    return app

if __name__ == '__main__':
    # Create the app
    app = create_app()

    # Run the Flask application
    app.run(debug=True)
