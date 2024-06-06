from flask import Flask
from flask_pymongo import PyMongo
from routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    mongo = PyMongo(app)

    init_routes(app, mongo)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)