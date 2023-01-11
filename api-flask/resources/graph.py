from itertools import combinations

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import NetworkSchema
from flask import jsonify

from globals import user

blp = Blueprint("graph", __name__, description="Operations on graph")

def norm_list(the_list, new_min_value=0, new_max_value=1, return_int = False):
  min_value = min(the_list)
  max_value = max(the_list)
  delta_value = max_value - min_value
  scaled_values = [ (v - min_value) / delta_value * (new_max_value - new_min_value) + new_min_value for v in  the_list]
  if return_int: scaled_values = [round(i) for i in scaled_values]
  return scaled_values

def get_group_coloring(src, groups: list, column_name: str):
    _colors={}
    colors = src.get_group_features(column_name=column_name, group_list=groups)
    for g, row_color  in colors.items():
      _colors[g]= sum([float(i) for i in row_color.values()]) / len(row_color.values())
    return _colors


def compute_group_centroid(node_group: dict, network_nodes: list):
  center_xs = []
  center_ys = []
  for node_id in node_group['node_ids']:
    center_xs.append(network_nodes[node_id]['x'])
    center_ys.append(network_nodes[node_id]['y'])


  x = round(sum(center_xs) / len(center_xs))
  y = round(-1 * sum(center_ys) / len(center_ys))
  
  return x, y

def get_simplied_group_network(src, name, color_name):
  nw = src.get_network(name=name)
  node_groups = nw.get_node_groups()

  _node_dict = {}
  for n in nw.nodes:
    _node_dict[int(n['id'])] = n

  groups = {}
  sizes = []
  centroid_x = []
  centroid_y = []

  for g in node_groups:
      grp = src.get_group(id=g['id'])
      groups[g['id']] = grp
      sizes.append(grp['row_count'])

      _x, _y = compute_group_centroid(g, _node_dict)
      centroid_x.append(_x)
      centroid_y.append(_y)

  scaled_sizes =  norm_list(sizes, 10, 30, True) #Mike requested the radius scale between 30 and 10
  centroid_x = norm_list(centroid_x, 5, 495, True)
  centroid_y = norm_list(centroid_y, 5, 295, True)

  combs = list(combinations(groups.keys(), 2))
  data = []
  nodes = []

  #create nodes with edges to self to ensure all groups make it into the graph
  #for instance a connected component that is one group would only show up here
  # since it would not have any conenctions to other groups
  group_colors = get_group_coloring(src, node_groups, color_name)
  group_colors_keys = [k for k in group_colors.keys()]

  group_colors_values = [group_colors[k] for k in group_colors_keys]
  scaled_group_colors = norm_list(group_colors_values, 0, 1)
  scaled_group_colors = dict(zip(group_colors_keys, scaled_group_colors))
 
  for e, k in enumerate(groups.keys()):
    nodes.append({'id': k, 'groupId': k, 'colorScale': scaled_group_colors[int(k)], "marker": { "radius": scaled_sizes[e]}, "plotX": centroid_x[e], "plotY": centroid_y[e]})

  #Create Nodes with edges
  for f, t in combs:
    if not set(groups[f]['row_indices']).isdisjoint(set(groups[t]['row_indices'])): data.append([f, t])
  
  return data, nodes

def get_normal_network(src, name, color_name):
  nw = src.get_network(name=name)

  #adds in all links
  '''
  data = data + [[0,11], [0,14], ..., [33, 62],...]
  '''
  data = [[ str(d['from']), str(d['to']) ] for d in nw.links]
    
  #scale sizes
  sizes = [d['row_count'] for d in nw.nodes]
  norm_sizes = norm_list(sizes, 2, 10)

  #get coloring values
  outcome_coloring = src.create_coloring(name=color_name, column_name=color_name)
  coloring_values = nw.get_coloring_values(name=color_name)
  #scale coloring between zero and 1
  norm_coloring_values = norm_list(coloring_values)

  #Get plotX and plotY values
  x = [v['x'] for v in nw.nodes]
  y = [-1*v['y'] for v in nw.nodes]
  x = norm_list(x, 5, 495, True)
  y = norm_list(y, 5, 295, True)

  nodes_id_to_group_id = {}
  for g in nw.node_groups:
      for ni in g['node_ids']:
          nodes_id_to_group_id[ni] = g['id']

  # get node dict
  #scale radius between 10 and 2
  nodes = [{'id': d['id'], 'groupId': nodes_id_to_group_id[int(d['id'])] if int(d['id']) in nodes_id_to_group_id else None, 'marker': { 'radius': norm_sizes[e] }, 'colorScale':  norm_coloring_values[e], "plotX": x[e], "plotY": y[e]} for e, d in enumerate(nw.nodes)]

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
            ['A', 'C']
            ['A', 'D'],
            ['A', 'E'],
            ['A', 'F'],
            ['A', 'G'],
            ['B', 'C'],
            ['B', 'D']
        ],
        nodes = [{
                      id: 'A',
                      colorIndex: 4.1,
                      readius: 21
                  }, {
                      id: 'B',
                      colorIndex: 2.4,
                      radius: 11.8
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
      
      if network_data['simplified']:
        print("Simplified")
      
        data, nodes = get_simplied_group_network(src, grp_name, network_data['color_name'])
      else:
        print("Regular")
        #get network nodes
        data, nodes = get_normal_network(src, grp_name, network_data['color_name'])

      network_data['data'] = data
      network_data['nodes'] = nodes

      return jsonify(network_data)

    except:
      abort(404, message="Error getting network graph from server")


@blp.route("/graph/color")
class GraphService(MethodView):
  @blp.arguments(NetworkSchema)
  # @blp.response(200, NetworkSchema)
  def post(self, network_data):
    """Returns nodes in this format for network graph
        filter_id: 123456,
        color_field: column_name,
        data = [
            ['A', 'C']
            ['A', 'D'],
            ['A', 'E'],
            ['A', 'F'],
            ['A', 'G'],
            ['B', 'C'],
            ['B', 'D']
        ],
        nodes = [{
                      id: 'A',
                      colorIndex: 4.1,
                      readius: 21
                  }, {
                      id: 'B',
                      colorIndex: 2.4,
                      radius: 11.8
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
      
      if network_data['simplified']:
        print("Simplified")
      
        data, nodes = get_simplied_group_network(src, grp_name, network_data['color_name'])
      else:
        print("Regular")
        #get network nodes
        data, nodes = get_normal_network(src, grp_name, network_data['color_name'])

      network_data['data'] = data
      network_data['nodes'] = nodes

      return jsonify(network_data)

    except:
      abort(404, message="Error getting network graph from server")
