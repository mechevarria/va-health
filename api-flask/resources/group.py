from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from globals import user


blp = Blueprint("group", __name__, description="Operations on groups")

def get_categorcial_column_list(column_names):
  #prefixes to use
  prefixes = [
  'VeteranFlag_',
  'PatientType_',
  'MaritalStatus_',
  'Gender_',
  'PeriodOfService_',
  'Eligibility_',
  'Race_',
  'Ethnicity_',
  'BloodType_',
  'Rurality_',
  'covid_vaccine_',
  'covid_symptomsseverity_',
  'covid_pre_',
  'covid_post_',
  'conditions_pre_',
  'meds_pre_',
  'meds_post_',
  'meds_',
  'modality_',
  ]

  cols_we_want = ['Medicaid', 'Medicare', 'OtherInsurance', 'NoRecordOfInsurance' ]

  #add all columns that start with the specified prefixes
  for p in prefixes:
    cols_we_want = cols_we_want + [c for c in column_names if c.startswith(p)]

  #add columns for visit_cols_prefixes and visit_cols_suffixes 
  cols_we_want = [c for c in cols_we_want if not c.endswith("OccurrenceType")]
  # cols_we_want = [c for c in cols_we_want if not c.endswith("change")]

  return cols_we_want

def get_continuous_column_list(column_names):
  #prefixes to use
  prefixes = [
  'vitals_',
  'A1C_',
  'A1Clast',
  'Risk_score_',
  # ]

  # #Need for each period 1/2/3
  # visit_cols_prefixes = [
  'visits_count_',
  'visits_count_permonth_',
  'visits_count_Phone_',
  'visits_count_Presumed In Person_',
  'visits_count_VVC_',
  'visits_count_permonth_Phone_',
  'visits_count_permonth_Presumed In Person_',
  'visits_count_permonth_VVC_',
  'visits_count_proportion_Phone_',
  'visits_count_proportion_Presumed In Person_',
  'visits_count_proportion_VVC_',
  'visits_count_comorbiditiescare_',
  'visits_count_directcare_',
  'visits_count_lifestylecare_',
  'visits_count_permonth_comorbiditiescare_',
  'visits_count_permonth_directcare_',
  'visits_count_permonth_lifestylecare_',
  'visits_count_proportion_comorbiditiescare_',
  'visits_count_proportion_directcare_',
  'visits_count_proportion_lifestylecare_',
  ]
  # visit_cols_suffixes = ['period1', 'period2', 'period3']
  # cols_we_want = ['AgeAtIndex', 'Is_increase_A1Clast_period3_to_4_change' , 'Is_decrease_visits_count_permonth_period3_to_4_change']
  cols_we_want = ['AgeAtIndex']

  #add all columns that start with the specified prefixes
  for p in prefixes:
    cols_we_want = cols_we_want + [c for c in column_names if c.startswith(p)]

  #add columns for visit_cols_prefixes and visit_cols_suffixes 
  # cols_we_want = cols_we_want + [p+s for p in visit_cols_prefixes for s in visit_cols_suffixes]  
  # cols_we_want = cols_we_want + [p+s for p in visit_cols_prefixes for s in visit_cols_suffixes]  
  cols_we_want = [c for c in cols_we_want if not 'period5' in c]
  print(cols_we_want)
  return cols_we_want

def get_group_details(src, group_1_id, group_2_id="Rest"):
  if group_2_id=="Rest":
    print("group 2 is REST")
    grp = src.get_group(id=group_1_id)
    _exp = {'id': grp['id'], 'primary_name': grp['id'], 'primary_size': grp['row_count'], 'secondary_name': 'Rest', 'secondary_size': src.row_count - grp['row_count']}

    #check to make sure comparison exists.  If not, create
    comp = src.get_comparison(name=f"{grp['name']} vs. Rest")

    if "msg" in comp:  #means dictionary returned with message saying compare does not exist
      comp = src.compare_groups(group_1_name=grp['name'],group_2_name="Rest", name=f"{grp['name']} vs. Rest", async_=False)
  else:
    print("group 2 is NOT rest")

    grp1 = src.get_group(id=group_1_id)
    grp2 = src.get_group(id=group_2_id)
    _exp = {'primary_name': grp['id'], 'primary_size': grp1['row_count'], 'secondary_name': grp2['id'], 'secondary_size': grp2['row_count']}

    comp = src.get_comparison(name=f"{grp1['name']} vs. {grp2['name']}")
    if "msg" in comp:  #means dictionary returned with message saying compare does not exist
      comp = src.compare_groups(group_1_name=grp1['name'],group_2_name=grp2['name'], name=f"{grp1['name']} vs. {grp2['name']}", async_=False)

    _exp['id'] = comp['id']
  
  _explainers = []

  #search continuous_explainers
  cols = get_continuous_column_list(src.column_names)
  for e in comp['continuous_explainers']:
    if e['name'] in cols:
      _ = {"type": "continuous", 'name': e['name'], 'primary_group_mean': e['primary_group_mean'], "primary_group_quartiles": e['quartiles'][0],
      'secondary_group_mean': e['secondary_group_mean'], "secondary_group_quartiles": e['quartiles'][1]}
      _explainers.append(_)

  #search cat_explainers
  cols = get_categorcial_column_list(src.column_names)
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