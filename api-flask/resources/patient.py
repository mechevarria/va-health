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

def get_carepath(d):
    _dict = {}
    #DIABETIC MEDS
    diabetic_med_keys = natural_sort([c for c in d.keys() if (c.startswith("meds_") 
                                                 and not c.startswith("meds_pre") 
                                                 and not c.startswith("meds_post") 
                                                 and not c.endswith("OccurrenceType") 
                                                 and not c.endswith("change"))])

    med_dict = OrderedDict((k, d[k]) for k  in diabetic_med_keys if d[k] > 0)

    diabetic_med_prefix = set([k.replace("_period1_2", '').replace("_period3", '') for k in med_dict.keys()])
    suffix = ["_period1_2","_period3"]
    _ = {}
    for mp in diabetic_med_prefix:
      _[mp.replace('meds_', "")]={}
      for s in suffix: _[mp.replace('meds_', "")][s] = med_dict.get(mp+s, 0)
            
    _dict['diabetic_meds'] = _
    print(_dict.keys())
    print(_dict)
    print()
    #NON diabetic meds
    non_diabetic_med_keys = natural_sort([c for c in d.keys() if (c.startswith("meds_pre") 
                                                 or c.startswith("meds_post") 
                                                 and not c.endswith("OccurrenceType") 
                                                 and not c.endswith("change"))])

    med_dict = OrderedDict((k, d[k]) for k  in non_diabetic_med_keys if d[k] > 0)

    non_diabetic_med_prefix = set([k.replace("meds_pre_", '').replace("meds_post_", '').replace("2yrs", '').replace("60dOrMore", '').replace("60d", '') for k in med_dict.keys()])
    _={}
    for mp in non_diabetic_med_prefix:
        pre = 0
        post = 0
        
        if f'meds_pre_{mp}2yrs' in med_dict.keys():
            pre = med_dict[f'meds_pre_{mp}2yrs']
        
        if f'meds_post_{mp}60d' in med_dict.keys():
            post = med_dict[f'meds_post_{mp}60d']

        elif f'meds_post_{mp}' in med_dict.keys():
            #check to see if post only
            post = med_dict[f'meds_post_{mp}']
        else:
            pass
        
            
        _[mp]={'pre': pre, 'post': post}

    _dict['meds'] = _
    print(_dict.keys())
    print(_dict)
    print()
    #Visits
    visit_keys = ['visits_count_Phone_period1', 'visits_count_Phone_period2', 'visits_count_Phone_period3',
                    'visits_count_Presumed In Person_period1', 'visits_count_Presumed In Person_period2', 'visits_count_Presumed In Person_period3',
                    'visits_count_VVC_period1', 'visits_count_VVC_period2', 'visits_count_VVC_period3',
                    'visits_count_comorbiditiescare_period1', 'visits_count_directcare_period1', 'visits_count_lifestylecare_period1',
                    'visits_count_comorbiditiescare_period2', 'visits_count_directcare_period2', 'visits_count_lifestylecare_period2',
                    'visits_count_comorbiditiescare_period3', 'visits_count_directcare_period3', 'visits_count_lifestylecare_period3'
                    ]

    visit_dict = OrderedDict((k, d[k]) for k  in visit_keys)

    visit_prefix = set([k.replace("_period1", '').replace("_period2", '').replace("_period3", '') for k in visit_dict.keys()])
    suffix = ["_period1", "_period2", "_period3"]
    
    _ = {}
    for kp in visit_prefix:
        #Check if prefix already in dict.  If not, then add
        if (kp) not in _: _[kp]={}
        for s in suffix: _[kp][s] = visit_dict.get(kp+s, 0)
    
    _dict['visits'] = _
    print(_dict.keys())
    print(_dict)
    print()
    return _dict

def get_consesus_carepath(d, behavior_keys):
    _dict = {}
    
    #get list of nearest neighbors ids
    nn_ids = [str(d[k]) for k in behavior_keys]

    src = user['connection'].get_source(name=user['source_name_holdout'])
    #create filter set based on ids
    fs = src.create_filter_set([{'column_name':"PatientICN", "in_set": nn_ids}])
    export = src.export(filter_set=fs)
    if len(export['data']) == 0: raise NameError(f"Patient neighbors not found!")

    #convert export to pandas dataframe
    cols = [src.id_to_colnames[i] for i in export['column_indices']]
    df = pd.DataFrame(export['data'], index=cols).T

    #get DIABETIC MED meds for carepath
    diabetic_med_keys = natural_sort([c for c in d.keys() if (c.startswith("meds_") 
                                                 and not c.startswith("meds_pre") 
                                                 and not c.startswith("meds_post") 
                                                 and not c.endswith("OccurrenceType") 
                                                 and not c.endswith("change"))])
    #compute the means of the diabetic meds
    diabetic_med_prefix = set([k.replace("_period1_2", '').replace("_period3", '') for k in diabetic_med_keys])
    suffix = ["_period1_2","_period3"]
    
    _ = {}
    for dmp in diabetic_med_prefix:
        _[dmp.replace('meds_', '')]={}
        for s in suffix: _[dmp.replace('meds_', '')][s] = df[dmp+s].sum()/100

    _dict['diabetic_meds'] = _

    #get NON DIABETIC MED meds for carepath
    #only show now diabetic meds with numbers > 0.7 for either pre/post
    non_diabetic_med_keys = natural_sort([c for c in d.keys() if (c.startswith("meds_pre") 
                                                 or c.startswith("meds_post") 
                                                 and not c.endswith("OccurrenceType") 
                                                 and not c.endswith("change"))])
    non_diabetic_med_prefix = set([k.replace("meds_pre_", '').replace("meds_post_", '').replace("2yrs", '').replace("60dOrMore", '').replace("60d", '') for k in non_diabetic_med_keys])

    _ = {}
    column_names = list(df.columns)
    for mp in non_diabetic_med_prefix:
        pre = 0
        post = 0
        
        if f'meds_pre_{mp}2yrs' in column_names:
            pre = df[f'meds_pre_{mp}2yrs'].sum()

        if f'meds_post_{mp}60d' in column_names:
            post = df[f'meds_post_{mp}60d'].sum()
            
        elif f'meds_post_{mp}' in column_names:
            #check to see if post only
            post = df[f'meds_post_{mp}'].sum()
        else:
            pass
            
        if (pre > 70 or post > 70):
            _[mp]={'pre': pre/100, 'post': post/100}
                      
    _dict['meds'] = _


    #Get consensus visits carepaths
    visit_prefix = ['visits_count_Phone', 'visits_count_Presumed In Person', 'visits_count_VVC',
              'visits_count_comorbiditiescare', 'visits_count_directcare', 'visits_count_lifestylecare']
    visit_suffix = ['period1', 'period2', 'period3']

    _={}
    for vp in visit_prefix:
      _[vp] = {}
      for vs in visit_suffix:
        _[vp][vs] = df[f'{vp}_{vs}'].mean()

    _dict['visits'] = _

    return _dict


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
        'Vaccination_Status':'covid_vaccine_TotalSeriesCount',
        'Race':'Race',
        'Ethnicity':'Ethnicity',
        'Marital_Status':'MaritalStatus',
        'Rurality':'Rurality',
        "A1C_Increase_Risk": "Risk_score_is_increase_A1Clast_period3_to_4_change",
        "Engagement_Decrease_Risk": "Risk_score_is_decrease_visits_count_permonth_period3_to_4_change"
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
    print("In call")
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
          "Over Weight": "Yes" if zipdict["conditions_pre_OverweightAtIndex"] == 1 else "No",
          "BMI": zipdict["vitals_BMIAtIndex"],
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

      return_data['comorbidities'] = {k.replace("conditions_pre_", ""): v for k, v in zipdict.items() if "conditions" in k and v == 1}
      return_data['carepath'] = get_carepath(zipdict)

      #TODO: need to get/specify behaviors
      if True:
        behavior_keys = [k for k in zipdict.keys() if k.startswith('nn1_')]
      else:
        behavior_keys = [k for k in zipdict.keys() if k.startswith('nn2_')]

      return_data['consensus_carepath'] = get_consesus_carepath(zipdict, behavior_keys)

      return return_data
    except NameError:
      abort(400, message=f"Patient ({patient_id}) not found!")

    except:
      abort(404, message=f"Error getting Patient ({patient_id}) data from source")
