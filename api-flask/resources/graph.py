from itertools import combinations

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify

from db import user

blp = Blueprint("graph", __name__, description="Operations on graph")

# @blp.route("/graph/<string:network_id>")
@blp.route("/graph")
class GraphService(MethodView):
  # def get(self, network_id):
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
    src = user['connection'].get_source(name=user['source_name'])
    #TODO: Remove hardwired and get id from user.  Once filter enabled
    network_id = "-4920673681958740057"
    nw = src.get_network(id=network_id)
    node_groups = nw.get_node_groups()
    print(len(node_groups))

    groups = {}
    for g in node_groups:
        grp = src.get_group(id=g['id'])
        g['rows'] = set(grp['row_indices'])
        groups[g['id']] = g
      
    combs = list(combinations(groups.keys(), 2))

    data = []

    #create nodes with edges to self to ensure all nodes make it into the graph
    for k in groups.keys():
      data.append({'from': k, 'to': k})

    #Create Nodes with edges
    for f, t in combs:
      if groups[f]['rows'].isdisjoint(groups[t]['rows']): data.append({'from': f, 'to': t})

    return jsonify(data)

