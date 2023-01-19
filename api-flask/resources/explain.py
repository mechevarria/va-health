from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ExplainerSchema

from globals import user


blp = Blueprint("explain", __name__, description="Operations on explains")

def get_compares(src, network_name):
  _explainers = []

  nw = src.get_network(name=network_name)
  node_groups = nw.get_node_groups()
  #get compare for each group
  # src.get_comparison(name='18310991_1 vs. Rest on All columns')
  for g in node_groups:
    grp = src.get_group(id=g['id'])
    _exp = {'id': grp['id'], 'name': grp['name'], 'group_size': grp['row_count']}

    comp = src.get_comparison(name=f"{grp['name']} vs. Rest on All columns")
    top_continuous_explainers = list(filter(lambda e: e['ks_score'] > 0.5, comp['continuous_explainers']))
    sorted_continuous_explainers = sorted(top_continuous_explainers, key=lambda d: d['ks_score'])
    sorted_continuous_explainers = [f"{c['name']} {'higher' if c['ks_sign']=='+' else 'lower'} than cohort -> {'Significant' if c['ks_score']>= 0.7 else 'Moderate'}" for c in sorted_continuous_explainers]
    
    top_cat_explainers = list(filter(lambda e: e['hypergeometric_p_values'][0] <= 0.05, comp['categorical_explainers']))
    sorted_cat_explainers = sorted(top_cat_explainers, key=lambda d: ['hypergeometric_p_values'][0])
    sorted_cat_explainers = [f"{c['name']} -> {c['percent_in_group'][0]*100: 0.1f}%, {c['percent_in_group'][1]*100: 0.1f}% in cohort" for c in sorted_cat_explainers]
    
    _exp['explains'] = sorted_continuous_explainers + sorted_cat_explainers
    _exp['explains'] =   _exp['explains'][0:10]

    _explainers.append(_exp)
  return _explainers

@blp.route("/explain")
class ExplainService(MethodView):
  @blp.response(200, ExplainerSchema(many=True))
  def get(self):
    '''Gets Top explainers for all groups in default netowrk'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      #TODO: Must use final network name for VA source
      #Place holder is OAA_1 here
      network_name = user['network_name']
      return get_compares(src, network_name)

    except Exception as e: 
      abort(http_status_code=404, message=str(e))


@blp.route("/explain/<string:filter_id>")
class FilteredExplainService(MethodView):
  '''Gets Top explainers for all groups the specified filter id'''
  @blp.response(200, ExplainerSchema(many=True))
  def get(self, filter_id):
    '''Gets all KPI values the source'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      grp = src.get_group(id=filter_id)
      network_name = grp['name']

      return get_compares(src, network_name)

    except Exception as e: 
      abort(http_status_code=404, message=str(e))