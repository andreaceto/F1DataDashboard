from flask import Blueprint, jsonify

def history_bp(mongo):
    bp = Blueprint('history', __name__)

    @bp.route('/api/history')
    def get_history():
        history = mongo.db.history.find()
        return jsonify([record for record in history])

    return bp