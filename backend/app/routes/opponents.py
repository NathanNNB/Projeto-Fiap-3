from flask import Blueprint, jsonify
from app.services.opponents import opponentsList
from flask_cors import CORS

opponents = CORS(Blueprint("opponents", __name__))

@opponents.route("/", methods=["GET"])
def listar_opponents():
    return jsonify({"opponents": opponentsList})