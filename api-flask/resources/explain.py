from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ExplainerSchema

from globals import user


blp = Blueprint("explain", __name__, description="Operations on explains")

# def get_compares(src, network_name):
#   _explainers = []

#   nw = src.get_network(name=network_name)
#   node_groups = nw.get_node_groups()
#   #get compare for each group
#   # src.get_comparison(name='18310991_1 vs. Rest on All columns')
#   for g in node_groups:
#     grp = src.get_group(id=g['id'])
#     _exp = {'id': grp['id'], 'name': grp['name'], 'group_size': grp['row_count']}

#     comp = src.get_comparison(name=f"{grp['name']} vs. Rest on All columns")
#     top_continuous_explainers = list(filter(lambda e: e['ks_score'] > 0.5, comp['continuous_explainers']))
#     sorted_continuous_explainers = sorted(top_continuous_explainers, key=lambda d: d['ks_score'])
#     sorted_continuous_explainers = [f"{c['name']} {'higher' if c['ks_sign']=='+' else 'lower'} than cohort -> {'Significant' if c['ks_score']>= 0.7 else 'Moderate'}" for c in sorted_continuous_explainers]
    
#     top_cat_explainers = list(filter(lambda e: e['hypergeometric_p_values'][0] <= 0.05, comp['categorical_explainers']))
#     sorted_cat_explainers = sorted(top_cat_explainers, key=lambda d: ['hypergeometric_p_values'][0])
#     sorted_cat_explainers = [f"{c['name']} -> {c['percent_in_group'][0]*100: 0.1f}%, {c['percent_in_group'][1]*100: 0.1f}% in cohort" for c in sorted_cat_explainers]
    
#     _exp['explains'] = sorted_continuous_explainers + sorted_cat_explainers
#     _exp['explains'] =   _exp['explains'][0:10]

#     _explainers.append(_exp)
#   return _explainers

# @blp.route("/explain")
# class ExplainService(MethodView):
#   @blp.response(200, ExplainerSchema(many=True))
#   def get(self):
#     '''Gets Top explainers for all groups in default netowrk'''
#     try:
#       src = user['connection'].get_source(name=user['source_name'])
#       network_name = user['network_name']
#       return get_compares(src, network_name)

#     except Exception as e: 
#       abort(http_status_code=404, message=str(e))

def get_compares(src, group_id):
  grp = src.get_group(id=group_id)
  _exp = {'id': grp['id'], 'name': grp['name'], 'group_size': grp['row_count']}

  comp = src.get_comparison(name=f"{grp['name']} vs. Rest")
  if "msg" in comp:  #means dictionary returned with message saying compare does not exist
      comp = src.compare_groups(group_1_name=grp['name'],group_2_name='Rest', name=f"{grp['name']} vs. Rest", async_=False)

  #signigicant explains have ks-score >= 0.7
  significant_continuous_explainers = list(filter(lambda e: e['ks_score'] >= 0.7, comp['continuous_explainers']))
  significant_continuous_explainers = sorted(significant_continuous_explainers, key=lambda d: d['ks_score'], reverse=True)
  significant_continuous_explainers = [f"{c['name']} {'higher' if c['ks_sign']=='+' else 'lower'} than cohort -> {'Significant' if c['ks_score']>= 0.7 else 'Moderate'}" for c in significant_continuous_explainers]

  #moderate explains have ks-score between 0.5 and 0.7
  moderate_continuous_explainers = list(filter(lambda e: (e['ks_score'] >= 0.5 and e['ks_score'] < 0.7), comp['continuous_explainers']))
  moderate_continuous_explainers = sorted(moderate_continuous_explainers, key=lambda d: d['ks_score'], reverse=True)
  moderate_continuous_explainers = [f"{c['name']} {'higher' if c['ks_sign']=='+' else 'lower'} than cohort -> {'Significant' if c['ks_score']>= 0.7 else 'Moderate'}" for c in moderate_continuous_explainers]

  #have geometric p value <= 0.5
  top_cat_explainers = list(filter(lambda e: e['hypergeometric_p_values'][0] <= 0.05, comp['categorical_explainers']))
  sorted_cat_explainers = sorted(top_cat_explainers, key=lambda d: d['hypergeometric_p_values'][0])
  sorted_cat_explainers = [f"{c['name']} -> {c['percent_in_group'][0]*100: 0.1f}%, {c['percent_in_group'][1]*100: 0.1f}% in cohort" for c in sorted_cat_explainers]
  
  #Takes signigicant cont then top categorical then moderate cont
  if len(significant_continuous_explainers) >= 10:
    _exp['explains'] = significant_continuous_explainers[0:10]
  elif len(significant_continuous_explainers) + len(sorted_cat_explainers) >= 10:
    _exp['explains'] = (significant_continuous_explainers + sorted_cat_explainers) [0:10]
  else:
    x = len(significant_continuous_explainers + sorted_cat_explainers)
    _exp['explains'] = significant_continuous_explainers + moderate_continuous_explainers[0:10-x] + sorted_cat_explainers 

  return _exp

@blp.route("/explain/<string:group_id>")
class FilteredExplainService(MethodView):
  '''Gets Top explainers for group'''
  @blp.response(200, ExplainerSchema)
  def get(self, group_id):
    '''Gets Top explainers for the group'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      return get_compares(src, group_id)

    except Exception as e: 
      abort(http_status_code=404, message=str(e))