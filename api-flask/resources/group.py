from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from globals import user


blp = Blueprint("group", __name__, description="Operations on groups")

def get_group_details(src, group_id):
  # here is the list of columns we want
  cols = ["MaritalStatus_MARRIED", "MaritalStatus_WIDOWED", 
          "MaritalStatus_NEVER MARRIED", "MaritalStatus_DIVORCED", 
          "AgeAtIndexDate", 
          "Rurality_SmallTownRural", "Rurality_Urban", "Rurality_CityTown", 
          "Ethnicity_HISPANIC OR LATINO", "Race_Asian", "Race_Black or African American", "Race_White", "Race_American Indian or Alaska Native", 
          "visits_count_proportion_Presumed In Person_period4_2021-03-01_2022-03-01", 
          "visits_count_proportion_VVC_period4_2021-03-01_2022-03-01", 
          "visits_count_proportion_Phone_period4_2021-03-01_2022-03-01"
          ]

  cols += [c for c in src.column_names if "30d" in c[-3:]]
  cols += [c for c in src.column_names if "60d" in c[-3:]]
  cols += [c for c in src.column_names if "2yrs" in c]
  #get compare for group
  # src.get_comparison(name='18310991_1 vs. Rest on All columns')
  grp = src.get_group(id=group_id)
  _exp = {'id': grp['id'], 'name': grp['name'], 'group_size': grp['row_count']}

  comp = src.get_comparison(name=f"{grp['name']} vs. Rest on All columns")
  #search continuous_explainers
  _explainers = []
  keys = ['name', 'primary_group_mean', 'secondary_group_mean']

  for e in comp['continuous_explainers']:
    if e['name'] in cols:
      _ = {"type": "continuous", 'name': e['name'], 'primary_group_mean': e['primary_group_mean'], "primary_group_quartiles": e['quartiles'][0],
      'secondary_group_mean': e['secondary_group_mean'], "secondary_group_quartiles": e['quartiles'][1]}
      _explainers.append(_)

  #search cat_explainers
  for e in comp['categorical_explainers']:
    if e['name'].split(' =')[0] in cols: 
      _ = {"type": "categorical", 'name': e['name'], 'primary_group_percent': round(e['percent_in_group'][0]*100,2), 'secondary_group_percent': round(e['percent_in_group'][1]*100,2)}
      _explainers.append(_)

  _exp['explains'] =   _explainers
  return _exp

@blp.route("/group/<string:group_id>")
class GroupDetailService(MethodView):
  '''Gets group details for group with the specified group id'''
  # @blp.response(200, ExplainerSchema(many=True))
  def get(self, group_id):
    '''Gets explaienrs for the group'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      return get_group_details(src, group_id)

    except:
      abort(404, message="Error getting explains from server")