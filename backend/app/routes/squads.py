from flask import Blueprint, jsonify
from app.services.squads import squadsList
from flask_cors import CORS

squads = Blueprint("squads", __name__)
CORS(squads)

@squads.route("/", methods=["GET"])
def list_squads():
    return jsonify({"squads": squadsList})