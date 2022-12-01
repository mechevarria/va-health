from itertools import combinations

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify

from globals import user, get_all_group_id

blp = Blueprint("graph", __name__, description="Operations on graph")

def get_simplied_group_network(src, name):
    nw = src.get_network(name=name)
    node_groups = nw.get_node_groups()

    groups = {}
    for g in node_groups:
        grp = src.get_group(id=g['id'])
        g['rows'] = set(grp['row_indices'])
        groups[g['id']] = g
      
    combs = list(combinations(groups.keys(), 2))

    data = []

    #create nodes with edges to self to ensure all groups make it into the graph
    #for instance a connected component that is one group would only show up here
    # since it would not have any conenctions to other groups
    for k in groups.keys():
      data.append({'from': k, 'to': k})

    #Create Nodes with edges
    for f, t in combs:
      if groups[f]['rows'].isdisjoint(groups[t]['rows']): data.append({'from': f, 'to': t})
    
    return data

@blp.route("/graph")
class GraphService(MethodView):
  def get(self):
    """Returns nodes in this format for network graph
        data = [
            {'from': 'A', 'to': 'C'},
            {'from': 'A', 'to': 'D'},
            {'from': 'A', 'to': 'E'},
            {'from': 'A', 'to': 'F'},
            {'from': 'A', 'to': 'G'},
            {'from': 'B', 'to': 'C'},
            {'from': 'B', 'to': 'D'}
        ]    
    """
    try:
      src = user['connection'].get_source(name=user['source_name'])
      #TODO: Must use final network name for VA source
      #Place holder is OAA_1 here
      grp_name = "OAA 1"

      return jsonify(get_simplied_group_network(src, grp_name))

    except:
      abort(404, message="Error getting network graph from server")

@blp.route("/graph/<string:filter_id>")
class GraphService(MethodView):
  def get(self, filter_id):
    """Returns nodes in this format for network graph
        data = [
            {'from': 'A', 'to': 'C'},
            {'from': 'A', 'to': 'D'},
            {'from': 'A', 'to': 'E'},
            {'from': 'A', 'to': 'F'},
            {'from': 'A', 'to': 'G'},
            {'from': 'B', 'to': 'C'},
            {'from': 'B', 'to': 'D'}
        ]    
    """
    try:
      src = user['connection'].get_source(name=user['source_name'])
      grp = src.get_group(id=filter_id)

      return jsonify(get_simplied_group_network(src, grp['name']))

    except:
      abort(404, message="Error getting network graph from server")