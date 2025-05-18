from flask import Blueprint, jsonify
from app.services.squads import squadsList
from flask_cors import CORS

squads = CORS(Blueprint("squads", __name__))

@squads.route("/", methods=["GET"])
def listar_squads():
    return jsonify({"squads": squadsList})