from flask import Blueprint, jsonify, request
from app.services.report import report_list
from flask_cors import CORS

report = Blueprint("report", __name__)

CORS(report)

@report.route("/", methods=["GET"])
def list_report():

#     field = request.args.get('field', default='', type=str)
#     squad = request.args.get('squad', default='', type=str)
#     opponent = request.args.get('opponent', default='', type=str)

# # SELECT DISTINCT formation from `fut.formacoes` WHERE id_time = 33 


    return jsonify({"report": report_list})