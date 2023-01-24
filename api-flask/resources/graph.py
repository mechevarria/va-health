import scipy.stats as stats
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

def scale_colors(colors):
  zscaled_colors = stats.zscore(colors)
  #using c/abs(c) to determine the sign of c 
  zscaled_colors = [c if abs(c) < 2 else c/abs(c) * 2 for c in stats.zscore(zscaled_colors)]
  return norm_list(zscaled_colors)

def get_group_coloring(src, nw, node_groups: list, column_name: str):
  outcome_coloring = src.create_coloring(name=column_name, column_name=column_name)
  coloring_values = nw.get_coloring_values(name=column_name)

  _colors={}
  for g in node_groups:  
    color = []
    for n in g['node_ids']:
      color.append(coloring_values[n])
  
    _colors[g['id']] = sum(color) / len(color)
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

def get_simplied_group_network(src, name, color_name, chart_width):

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
  centroid_x = norm_list(centroid_x, 5, chart_width, True)
  centroid_y = norm_list(centroid_y, 5, 295, True)

  combs = list(combinations(groups.keys(), 2))
  data = []
  nodes = []

  group_colors = get_group_coloring(src, nw, node_groups, color_name)
  scaled_group_colors = scale_colors(list(group_colors.values()))
  scaled_group_colors = dict(zip(group_colors.keys(), scaled_group_colors))

  for e, k in enumerate(groups.keys()):
    nodes.append({'id': k, 'groupId': k, 'colorScale': scaled_group_colors[k], "marker": { "radius": scaled_sizes[e]}, "plotX": centroid_x[e], "plotY": centroid_y[e]})

  #Create Nodes with edges
  for f, t in combs:
    if not set(groups[f]['row_indices']).isdisjoint(set(groups[t]['row_indices'])): data.append([f, t])
  
  return data, nodes

def get_normal_network(src, name, color_name, chart_width):
  nw = src.get_network(name=name)

  all_node_ids= set(range(nw.node_count))

  #get all nodes with edges to remove singletons
  nodes_with_edges_ids = set()
  for link in nw.links:
    nodes_with_edges_ids.add(link['from'])
    nodes_with_edges_ids.add(link['to'])  

  singleton_node_ids = all_node_ids.difference(nodes_with_edges_ids)

  #get list of non-sigleton nodes
  #adds in all links
  '''
  data = data + [[0,11], [0,14], ..., [33, 62],...]
  '''
  data = [[ str(d['from']), str(d['to']) ] for d in nw.links]

  #scale sizes
  sizes = [d['row_count'] for d in nw.nodes] 
  #Add another value and scale for the size of the singletons
  if len(singleton_node_ids) > 0:
    if max(sizes) < len(singleton_node_ids):
      #create a node just a little bigger than biggest
      sizes = sizes + [max(sizes)*1.05] 

    else:
      #create a node the correct size
      sizes = sizes + [len(singleton_node_ids)] 
  
  norm_sizes = norm_list(sizes, 2, 10)

  #get coloring values
  outcome_coloring = src.create_coloring(name=color_name, column_name=color_name)
  coloring_values = nw.get_coloring_values(name=color_name)
  #scale coloring between zero and 1
  norm_coloring_values = scale_colors(coloring_values)
  #Get plotX and plotY values
  if len(singleton_node_ids) > 0:
    #Singleton points, need to add extra point
    x = [v['x'] for v in nw.nodes] + [sum([v['x'] for v in nw.nodes if int(v['id']) in singleton_node_ids]) / len(singleton_node_ids)]
    y = [-1*v['y'] for v in nw.nodes] + [sum([-1*v['y'] for v in nw.nodes if int(v['id']) in singleton_node_ids]) / len(singleton_node_ids)]
  else:
    #No singleton points, no need to add extra point
    x = [v['x'] for v in nw.nodes]
    y = [-1*v['y'] for v in nw.nodes]

  x = norm_list(x, 5, chart_width, True)
  y = norm_list(y, 5, 295, True)

  #Singletons should not be in a group
  nodes_id_to_group_id = {}
  for g in nw.node_groups:
      for ni in g['node_ids']:
          nodes_id_to_group_id[ni] = g['id']

  # get node dict
  #scale radius between 10 and 2
  nodes = [{'id': d['id'], 'groupId': nodes_id_to_group_id[int(d['id'])] if int(d['id']) in nodes_id_to_group_id else None, 
              'marker': { 'radius': norm_sizes[e] }, 'colorScale':  norm_coloring_values[e], "plotX": x[e], "plotY": y[e]} 
              for e, d in enumerate(nw.nodes) if e in nodes_with_edges_ids]
  

  #add one singleton node that contains all singletons
  #get singlton centroid
  # singleton_nodes = [n for n in nw.nodes if int(n['id']) in singleton_node_ids]
  if len(singleton_node_ids) > 0:
    sing_x = x[-1]
    sing_y = y[-1]

    #compute average node color for singleotn nodes
    sing_color = [norm_coloring_values[e] for e in singleton_node_ids]
    sing_color = sum([norm_coloring_values[e] for e in singleton_node_ids]) / len(singleton_node_ids)
    
    sing_size = norm_sizes[-1]  #added extra size for singltons above

    #add singlton node to list 
    nodes = nodes + [{'id': 'Singletons', 'groupId': None, 
                 'marker': { 'radius': sing_size }, 'colorScale':  sing_color, "plotX": sing_x, "plotY": sing_y} ]

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

      print("network_data: ", network_data)
      if "filter_id" in network_data:
        grp = src.get_group(id=network_data['filter_id'])
        grp_name = grp['name']
      else:
        grp_name = user['network_name']
      
      if network_data['simplified']:
        print("Simplified")
      
        data, nodes = get_simplied_group_network(src, grp_name, network_data['color_name'], network_data['chart_width'])
      else:
        print("Regular")
        #get network nodes
        data, nodes = get_normal_network(src, grp_name, network_data['color_name'], network_data['chart_width'])

      network_data['data'] = data
      network_data['nodes'] = nodes

      return jsonify(network_data)
    except Exception as e: 
      abort(http_status_code=404, message=f"Error getting network graph from server. Error: {str(e)}")
