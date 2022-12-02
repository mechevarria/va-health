from itertools import combinations

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import NetworkSchema
from flask import jsonify

from globals import user, get_all_group_id

blp = Blueprint("graph", __name__, description="Operations on graph")

def get_group_coloring(src, groups: list, column_name: str):
    _colors={}
    colors = src.get_group_features(column_name=column_name, group_list=groups)
    for g, row_color  in colors.items():
      _colors[g]= sum([float(i) for i in row_color.values()]) / len(row_color.values())
    return _colors


def get_simplied_group_network(src, name, color_name):
    nw = src.get_network(name=name)
    node_groups = nw.get_node_groups()

    groups = {}
    for g in node_groups:
        grp = src.get_group(id=g['id'])
        g['rows'] = set(grp['row_indices'])
        groups[g['id']] = g
      
    combs = list(combinations(groups.keys(), 2))

    data = []
    nodes = []

    #create nodes with edges to self to ensure all groups make it into the graph
    #for instance a connected component that is one group would only show up here
    # since it would not have any conenctions to other groups
    group_colors = get_group_coloring(src, node_groups, color_name)

    for k in groups.keys():
      data.append([k, k])
      nodes.append({'id': k, 'colorIndex': group_colors[int(k)]})

    #Create Nodes with edges
    for f, t in combs:
      if not groups[f]['rows'].isdisjoint(groups[t]['rows']): data.append([f, t])
    
    return data, nodes

@blp.route("/graph")
class GraphService(MethodView):
  @blp.arguments(NetworkSchema)
  # @blp.response(200, NetworkSchema)
  def post(self, network_data):
    """Returns nodes in this format for network graph
        filter_id: 123456,
        color_field: column_name,
        data = [
            {'from': 'A', 'to': 'C', 'color': },
            {'from': 'A', 'to': 'D'},
            {'from': 'A', 'to': 'E'},
            {'from': 'A', 'to': 'F'},
            {'from': 'A', 'to': 'G'},
            {'from': 'B', 'to': 'C'},
            {'from': 'B', 'to': 'D'}
        ],
        nodes = [{
                      id: 'A',
                      colorIndex: 4.1
                  }, {
                      id: 'B',
                      colorIndex: 2.4
        }]   
    """
    try:
      src = user['connection'].get_source(name=user['source_name'])

      if "filter_id" in network_data:
        grp = src.get_group(id=network_data['filter_id'])
        grp_name = grp['name']
      else:
        #TODO: Must use final network name for VA source
        #Place holder is OAA_1 here
        grp_name = "OAA 1"
      
      data, nodes = get_simplied_group_network(src, grp_name, network_data['color_name'])
      network_data['data'] = data
      network_data['nodes'] = nodes
      
      return jsonify(network_data)

    except:
      abort(404, message="Error getting network graph from server")
