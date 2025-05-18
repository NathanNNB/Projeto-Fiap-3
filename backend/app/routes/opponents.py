from flask import Blueprint, jsonify
from app.services.opponents import opponentsList
from flask_cors import CORS

opponents = Blueprint("opponents", __name__)
CORS(opponents)

@opponents.route("/", methods=["GET"])
def list_opponents():
    return jsonify({"opponents": opponentsList})