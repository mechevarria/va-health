from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from schemas import ExplainerSchema

from globals import user


blp = Blueprint("explain", __name__, description="Operations on explains")

def get_compares(src, network_name):
  # TODO:
  #  Get network(Done)
  # Get network node groups(Done)
  # get explain for each group(Done)
  #filter out top explains
  #decide on return
  #High/Med/Low
  #Higher / Lower than rest
  #What about categorical
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
    top_continuous_explainers = [f"{c['name']} {'higher' if c['ks_sign']=='+' else 'lower'} than cohort -> {'Significant' if c['ks_score']>= 0.7 else 'Moderate'}" for c in top_continuous_explainers]
    _exp['explains'] = top_continuous_explainers
    #TODO - categorical explainers

    _explainers.append(_exp)
  return _explainers

@blp.route("/explain")
class ExplainService(MethodView):
  # @blp.response(200, ExplainerSchema(many=True))
  def get(self):
    print("In Explain")

    '''Gets Top explainers for all groups in default netowrk'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      #TODO: Must use final network name for VA source
      #Place holder is OAA_1 here
      network_name = "OAA 1"
      print(network_name)
      return jsonify(get_compares(src, network_name))

    except:
      abort(404, message="Error getting explains from server")


@blp.route("/explain/<string:filter_id>")
class FilteredExplainService(MethodView):
  '''Gets Top explainers for all groups the specified filter id'''
  # @blp.response(200, ExplainerSchema(many=True))
  def get(self, filter_id):
    '''Gets all KPI values the source'''
    try:
      src = user['connection'].get_source(name=user['source_name'])
      grp = src.get_group(id=filter_id)
      network_name = grp['name']

      return get_compares(src, network_name)

    except:
      abort(404, message="Error getting explains from server")