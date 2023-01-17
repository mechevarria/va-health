import pandas as pd
from collections import OrderedDict

import re

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PatientCardSchema

from globals import user, get_all_group_id

blp = Blueprint("patient", __name__, description="Operations on Patients")

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)

def group_stat(src, grp, column_name):
  _= src.get_group_features(column_name=column_name, group_list=[grp])
  values = [v for v in _[list(_.keys())[0]].values()]
  return values

def get_bloodtype(dict):
  bt_dict = {k: dict.get(k, None) for k in dict.keys() if "BloodType_" in k}

  bt = [k for k, v in bt_dict.items() if v]
  if bt:
    bt = bt[0].replace("BloodType_", "").replace(" Pos", '+').replace(" Neg", '-')
    return bt
  else:
    return None

@blp.route("/patient")
class DefaultPatientService(MethodView):
  @blp.response(200, PatientCardSchema(many=True))
  def get(self):
    '''Gets all patients from the source'''
    try:
      patients = {}
      values = {}

      src = user['connection'].get_source(name=user['source_name_holdout'])
      grp_id = get_all_group_id(src)['id']
      grp = src.get_group(id=grp_id)

      columns = {
        'ID':'PatientICN',
        'Gender': 'Gender_M',
        "Age": "AgeAtIndexDate",
        'Vaccination_Status':'TotalSeriesCount',
        'Race':'Race',
        'Ethnicity':'Ethnicity',
        'Marital_Status':'MaritalStatus',
        'Rurality':'Rurality',
      }

      for k, v in columns.items():
        #Convert to int
        if k in ['ID', 'Gender', 'Age', 'Vaccination_Status']:
          _ = [int(i) for i in group_stat(src, grp, v)]
        #Convert to string
        else:
          _ = [str(i) for i in group_stat(src, grp, v)]
        if k == "Gender":
          _ = ["Male" if (i == 1) else "Female" for i in _ ]
        values[k] = _


      df = pd.DataFrame(values)
      df.apply(pd.Series.explode).to_dict(orient='records')

      return df.to_dict(orient='records')

    except:
      abort(404, message="Error getting Patients from source")


@blp.route("/patient/<string:patient_id>")
class DetailedPatientService(MethodView):
  '''Gets patient detail values the specific patient id'''
  @blp.response(200)
  def get(self, patient_id):
    '''Gets all KPI values the source'''
    try:
      return_data = {}

      src = user['connection'].get_source(name=user['source_name_holdout'])
      fs = src.create_filter_set([{'column_name':"PatientICN", "in_set": [str(patient_id)]}])
      export = src.export(filter_set=fs)
      if len(export['data']) == 0: raise NameError(f"Patient ({patient_id})not found!")
      
      keys = [src.id_to_colnames[cid] for cid in export['column_indices']]
      values = [d[0] for d in export['data']]

      zipped = zip(keys,values)
      zipdict = dict(zipped)

      #patient physical details
      return_data['physical'] = {
          "Age": zipdict["AgeAtIndexDate"],
          "Over Weight": "Yes" if zipdict["OverweightAtIndex"] == 1 else "No",
          "BMI": zipdict["BMIAtIndex"],
          "Gender": "Male" if zipdict["Gender_M"] == 1 else "Female",
          "BloodType": get_bloodtype(zipdict)
          }

      #patient demographic details
      return_data['demographics'] = {
          "Race": zipdict["Race"],
          "Ethnicity": zipdict["Ethnicity"],
          "Marital Status": zipdict["MaritalStatus"],
          "Rurality": zipdict["Rurality"],
          }

      #predictive risk scores
      return_data['risk_scores'] = {
          "a1c_increase_risk": zipdict["Risk_score_is_increase_A1Clast_period3_to_4_change"],
          "engagement_decrease_risk": zipdict["Risk_score_is_decrease_visits_count_permonth_period3_to_4_change"]
          }

      return_data['raw'] = zipdict

      return_data['comorbidities'] = {k: v for k, v in zipdict.items() if "2yrs" in k and v == 1}
      
      carepath_keys = natural_sort([c for c in zipdict.keys() if c.startswith("meds_")] + [c for c in zipdict.keys() if c.startswith("visits_count_V")])

      return_data['carepath'] = OrderedDict((k, zipdict[k]) for k  in carepath_keys if zipdict[k] > 0)

      return return_data
    except NameError:
      abort(400, message=f"Patient ({patient_id}) not found!")

    except:
      abort(404, message=f"Error getting Patient ({patient_id}) data from source")
