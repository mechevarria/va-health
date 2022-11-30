from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from schemas import KpiCardSchema

from db import user

blp = Blueprint("kpi", __name__, description="Operations on kpi")

@blp.route("/kpi")
class KPIService(MethodView):
  def group_stat(self, src, grp, column_name):
    _= src.get_group_features(column_name=column_name, group_list=[grp])
    values = [float(v) for v in _[list(_.keys())[0]].values()]
    return values

  @blp.response(200, KpiCardSchema(many=True))
  def get(self):
    '''Gets all KPI values for the entire source'''
    try:
      kpis = []

      src = user['connection'].get_source(name=user['source_name'])

      #TODO: update based on filter
      grp = src.get_group("all_rows")

      #Get number of rows
      #TODO: update based on filter
      kpis.append({"name": "Total Patients", "value": grp['row_count']})

      #Get number of vaccinated
      vac_values = self.group_stat(src, grp, 'vaccination_status')
      vac_percent = sum(vac_values) / len(vac_values) 
      kpis.append({"name": "Vaccination Precentage", "value": vac_percent})
      
      #Get Hospitilization rate
      hr = self.group_stat(src, grp, 'hopitilization')
      hrp = sum(hr) / len(hr) 
      kpis.append({"name": "Hospitilization Rate", "value": hrp})

      #TODO: Visit type (3 seperate cards or 1 card?)
      kpis.append({"name": "Visit Type %", "value": -1})

      #Get average a1c for the group
      a1c = self.group_stat(src, grp, 'a1c')
      a1c = sum(a1c) / len(a1c) 
      kpis.append({"name": "Average A1C", "value": -a1c})

      return kpis

    except Exception as ex:
      print(ex)
      abort(404, message="Error getting KPI from source")





