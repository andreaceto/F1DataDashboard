from .home_routes import home_bp
from .race_routes import race_bp
from .team_routes import team_bp
from .calendar_routes import calendar_bp
from .history_routes import history_bp

def init_routes(app, mongo):
    app.register_blueprint(home_bp(mongo))
    app.register_blueprint(race_bp(mongo))
    app.register_blueprint(team_bp(mongo))
    app.register_blueprint(calendar_bp(mongo))
    app.register_blueprint(history_bp(mongo))