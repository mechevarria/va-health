from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
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
  vac_values = group_stat(src, grp, 'TotalSeriesCount')
  vac_percent = sum([i>0 for i in vac_values]) / len(vac_values) * 100
  kpis.append({"name": "Vaccination Precentage", "value": f"{vac_percent:.1f}%"})
  
  #Get Hospitilization rate
  hr = group_stat(src, grp, 'Hospitalization60d')
  hrp = sum(hr) / len(hr) * 100 
  kpis.append({"name": "Hospitilization Rate", "value":  f"{hrp:.1f}%"})

  in_per_vis = group_stat(src, grp, 'visits_count_proportion_Presumed In Person_period4_2021-03-01_2022-03-01')
  in_per_vis = sum(in_per_vis) / len(in_per_vis) * 100
  kpis.append({"name": "In Person Visit %", "value": f"{in_per_vis:.1f}%"})

  #Get average a1c for the group
  a1c = group_stat(src, grp, 'A1C_last_period4_2021-03-01_2022-03-01')
  a1c = sum(a1c) / len(a1c) 
  kpis.append({"name": "Average A1C", "value": f"{a1c:.2f}"})

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


@blp.route("/kpi/<string:filter_id>")
class FilteredKPIService(MethodView):
  '''Gets all KPI values the specific filter id'''

  @blp.response(200, KpiCardSchema(many=True))
  def get(self, filter_id):
    '''Gets all KPI values the source'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      kpis = compute_kpis(src, filter_id)
      return kpis
    except:
      abort(404, message="Error getting KPI from source")