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
    sizes = []
    for g in node_groups:
        grp = src.get_group(id=g['id'])
        groups[g['id']] = grp
        sizes.append(grp['row_count'])
      
    combs = list(combinations(groups.keys(), 2))
    data = []
    nodes = []

    min_size = min(sizes)
    max_size = max(sizes)

    #create nodes with edges to self to ensure all groups make it into the graph
    #for instance a connected component that is one group would only show up here
    # since it would not have any conenctions to other groups
    group_colors = get_group_coloring(src, node_groups, color_name)

    for k in groups.keys():
      size = (groups[k]['row_count'] - min_size) / (max_size - min_size) * (30-10) + 10   #Mike requested the radius scale between 30 and 10
      data.append([k, k])
      nodes.append({'id': k, 'colorIndex': group_colors[int(k)], "radius": size})

    #Create Nodes with edges
    for f, t in combs:
      if not set(groups[f]['row_indices']).isdisjoint(set(groups[t]['row_indices'])): data.append([f, t])
    
    return data, nodes

def get_normal_network(src, name, color_name):
  nw = src.get_network(name=name)

  #all node pairs to self, so all nodes are accounted for even singletons
  '''
  data = [[0,0], [1,1], ..., [nw.node_count -1, nw.node_count-1]]
  '''
  data=[[i,i] for i in range(nw.node_count)] 

  #adds in all links
  '''
  data = data + [[0,11], [0,14], ..., [33, 62],...]
  '''
  data += [[d['from'], d['to']] for d in nw.links]
    
  #get min / max sizes
  sizes = [d['row_count'] for d in nw.nodes]
  min_size = min(sizes)
  max_size = max(sizes)
  delta_size = max_size-min_size

  #get coloring values
  outcome_coloring = src.create_coloring(name=color_name, column_name=color_name)
  coloring_values = nw.get_coloring_values(name=color_name)
  #scale colring between zero and 1
  min_color = min(coloring_values)
  max_color = max(coloring_values)
  delta_color = max_color - min_color
  coloring_values = [ (c - min_color) / delta_color for c in  coloring_values]

  # get node dict
  #scale radius between 10 and 2
  nodes = [{'id': d['id'], 'radius': (d['row_count'] - min_size) / delta_size * (10-2) + 2, 'colorIndex':  coloring_values[e]} for e, d in enumerate(nw.nodes)]

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
