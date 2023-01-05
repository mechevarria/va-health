import pandas as pd
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PatientCardSchema

from globals import user, get_all_group_id

blp = Blueprint("patient", __name__, description="Operations on Patients")

def group_stat(src, grp, column_name):
  _= src.get_group_features(column_name=column_name, group_list=[grp])
  values = [v for v in _[list(_.keys())[0]].values()]
  return values

@blp.route("/patient")
class DefaultPatientService(MethodView):
  @blp.response(200, PatientCardSchema(many=True))
  def get(self):
    '''Gets all patients from the source'''
    try:
      patients = {}
      values = {}

      src = user['connection'].get_source(name=user['source_name'])
      grp_id = get_all_group_id()['id']
      grp = src.get_group(id=grp_id)

      columns = {
        'ID':'PatientCN',
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

      src = user['connection'].get_source(name=user['source_name'])
      fs = src.create_filter_set([{'column_name':"PatientCN", "in_set": [str(patient_id)]}])
      export = src.export(filter_set=fs)
      if len(export['data']) == 0: raise NameError(f"Patient ({patient_id})not found!")
      
      keys = [src.id_to_colnames[cid] for cid in export['column_indices']]
      values = [d[0] for d in export['data']]

      zipped = zip(keys,values)
      zipdict = dict(zipped)
      zipdict
      return zipdict
    except NameError:
      abort(400, message=f"Patient ({patient_id}) not found!")

    except:
      abort(404, message=f"Error getting Patient ({patient_id}) data from source")