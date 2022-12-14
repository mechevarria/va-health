from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from globals import user


blp = Blueprint("group", __name__, description="Operations on groups")

def get_group_details(src, group_1_id, group_2_id="Rest"):
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

  if group_2_id=="Rest":
    print("group 2 is REST")
    grp = src.get_group(id=group_1_id)
    _exp = {'id': grp['id'], 'primary_name': grp['name'], 'primary_size': grp['row_count'], 'secondary_name': 'Rest', 'secondary_size': src.row_count - grp['row_count']}

    #check to make sure comparison exists.  If not, create
    comp = src.get_comparison(name=f"{grp['name']} vs. Rest on All columns")

    if "msg" in comp:
      comp = src.compare_groups(group_1_name=grp['name'],group_2_name="Rest", async_=False)
  else:
    print("group 2 is NOT rest")

    grp1 = src.get_group(id=group_1_id)
    grp2 = src.get_group(id=group_2_id)
    _exp = {'primary_name': grp1['name'], 'primary_size': grp1['row_count'], 'secondary_name': grp2['name'], 'secondary_size': grp2['row_count']}

    comp = src.get_comparison(name=f"{grp1['name']} vs. {grp2['name']} on All columns")
    if "msg" in comp:
      comp = src.compare_groups(group_1_name=grp1['name'],group_2_name=grp2['name'], async_=False)

    _exp['id'] = comp['id']
  
  #search continuous_explainers
  _explainers = []
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
  '''Gets group details for group with the specified group id(s)
  if group_id is just one id 
    /group/123456 
    then it will be groupid vs rest

  if two ids sepereated by hyphen
    /group/123456-978654
    then it will be group 123456 vs group 987654
  '''
  # @blp.response(200, ExplainerSchema(many=True))
  def get(self, group_id):
    '''Gets explaienrs for the group'''
    try:
      src = user['connection'].get_source(name=user['source_name'])

      if "-" in group_id:
        _ = group_id.split("-")
        g1 = _[0]
        g2 = _[1]

        if g1 == g2: g2 = "Rest"
      else:
        g1 = group_id
        g2 = "Rest"
      
      return get_group_details(src, g1, g2)

    except:
      abort(404, message="Error getting explains from server")