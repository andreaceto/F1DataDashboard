from flask import Blueprint, jsonify

def home_bp(mongo):
    bp = Blueprint('home', __name__)

    @bp.route('/api/home')
    def home():
        drivers = mongo.db.drivers.find()
        return jsonify([driver for driver in drivers])

    return bp