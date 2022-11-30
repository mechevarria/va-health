from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from schemas import KpiCardSchema

from globals import user, get_all_group_id


blp = Blueprint("kpi", __name__, description="Operations on kpi")

def group_stat(src, grp, column_name):
  _= src.get_group_features(column_name=column_name, group_list=[grp])
  values = [float(v) for v in _[list(_.keys())[0]].values()]
  return values

def compute_kpis(src, group_id):
  kpis = []
  grp = src.get_group(id=group_id)

  kpis.append({"name": "Total Patients", "value": grp['row_count']})

  #Get number of vaccinated
  vac_values = group_stat(src, grp, 'vaccination_status')
  vac_percent = sum(vac_values) / len(vac_values) 
  kpis.append({"name": "Vaccination Precentage", "value": vac_percent})
  
  #Get Hospitilization rate
  hr = group_stat(src, grp, 'hopitilization')
  hrp = sum(hr) / len(hr) 
  kpis.append({"name": "Hospitilization Rate", "value": hrp})

  #TODO: Visit type (3 seperate cards or 1 card?)
  kpis.append({"name": "Visit Type %", "value": -1})

  #Get average a1c for the group
  a1c = group_stat(src, grp, 'a1c')
  a1c = sum(a1c) / len(a1c) 
  kpis.append({"name": "Average A1C", "value": a1c})

  return kpis

@blp.route("/kpi")
class DefaultKPIService(MethodView):
  @blp.response(200, KpiCardSchema(many=True))
  def get(self):
    '''Gets all KPI values the source'''
    try:
      kpis = []

      src = user['connection'].get_source(name=user['source_name'])
      grp_id = get_all_group_id()['id']
      kpis = compute_kpis(src, grp_id)

      return kpis

    except:
      abort(404, message="Error getting KPI from source")


# @blp.route("/kpi/<string:filter_id>")
# class Item(MethodView):
#     @blp.response(200, ItemSchema)
#     def get(self, item_id):

@blp.route("/kpi/<string:filter_id>")
class FilteredKPIService(MethodView):
  '''Gets all KPI values the speficief filter id'''

  @blp.response(200, KpiCardSchema(many=True))
  def get(self, filter_id):
    '''Gets all KPI values the source'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      kpis = compute_kpis(src, filter_id)
      return kpis
    except:
      abort(404, message="Error getting KPI from source")