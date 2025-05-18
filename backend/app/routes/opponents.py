from flask import Blueprint, jsonify
from app.services.opponents import opponentsList

opponents = Blueprint("opponents", __name__)

@opponents.route("/", methods=["GET"])
def listar_opponents():
    return jsonify({"opponents": opponentsList})