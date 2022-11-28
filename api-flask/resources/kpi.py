from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from schemas import KpiCardSchema

from db import user

blp = Blueprint("kpi", __name__, description="Operations on kpi")

@blp.route("/kpi")
class KPIService(MethodView):
  @blp.response(200, KpiCardSchema(many=True))
  def get(self):
    '''Gets all KPI values for the entire source'''
    print('in kpi')
    src = user['connection'].get_source(name=user['source_name'])
    src.row_count()

    #Get number of rows
    kpis.append({"name": "Total Patients", "value": src.row_count})
    kpis.append({"name": "Vaccination Precentage", "value": -1})
    kpis.append({"name": "Hospitilization Rate", "value": -1})
    kpis.append({"name": "Outpatient Visits", "value": -1})
    kpis.append({"name": "TBD", "value": -1})

    return kpis




