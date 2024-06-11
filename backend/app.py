from flask import Flask
from routes import home_route, raceStats_route, teamSection_route, calendar_route, history_route

# Create a Flask application instance
app = Flask(__name__)

# Register blueprints for different routes
app.register_blueprint(home_route.home_bp, url_prefix='/api/home')
app.register_blueprint(raceStats_route.race_stats_bp, url_prefix='/api/racestats')
app.register_blueprint(teamSection_route.team_section_bp, url_prefix='/api/teams')
app.register_blueprint(calendar_route.calendar_bp, url_prefix='/api/calendar')
app.register_blueprint(history_route.history_bp, url_prefix='/api/history')

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
