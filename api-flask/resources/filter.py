from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import FilterSchema, AppliedFilter

from globals import user, get_all_group_id

blp = Blueprint("filter", __name__, description="Operations on filters")

@blp.route("/filter")
class FilterService(MethodView):
  def generate_filter_name(self, filters):
    '''
    Returns a unique named based on filter values

    paramaters 
    filters: a list of FilterSchema
    '''
    _name = []
    for filter in filters:
      if filter['categorical']:
        _name.append('_'.join([filter['name'], 'IS' if  filter['is_equal'] else 'isNOT', str(filter['value'])]))
      else:
        _name.append('_'.join([filter['name'], str(filter['min']), 'to', str(filter['max'])]))

    return '; '.join(_name)

  def generate_filter_dict(self, filters):
    '''
    Returns a list of dictionaries formated for the platform sdk
    this list of dictionaries can be used to create a filter_set in the platform and then the filter
    set can be used to generate a group

    paramaters 
    filters: a list of FilterSchema
    '''
    _fds = []
    for filter in filters:
      if filter['categorical']:
        _fds.append({"column_name": filter["name"], "in_set": [filter['value']], "not": not filter["is_equal"]})
      else:
        _fds.append({"column_name": filter["name"], "in_range": [filter["min"], filter["max"]]})

    return _fds

  @blp.response(200, AppliedFilter)
  def get(self):
    '''Returns the ID for the default group / no filters applied'''
    return get_all_group_id()

  @blp.arguments(FilterSchema(many=True))
  @blp.response(200, AppliedFilter)
  def post(self, filter_data):
    #check each filter to make sure categorical and numeric formatted correctly
    for filter in filter_data:
      if filter['categorical']:
        if not('value' in filter.keys() and 'is_equal' in filter.keys()):
          abort(400, message=f"Filter {filter['name']} is missing either value of is_equal fields -> {filter}")
      else:
        if not('min' in filter.keys() and 'max' in filter.keys()):
          abort(400, message=f"Filter {filter['name']} is missing either min or max fields -> {filter}")

    try:
      name = self.generate_filter_name(filter_data)
      #check to see if filter has already been applied
      src = user['connection'].get_source(name=user['source_name'])
      grp = src.get_group(name=name)

      #note: is group not found returns {'msg': 'Group with given parameter does not exist'}
      #if found it returns the group dict
      if "id" not in grp.keys():
        #create a filter set
        fs = src.create_filter_set(self.generate_filter_dict(filter_data))
        #Create the groups from the filters
        grp = src.create_group(name=name, filter_set=fs)

      applied_filter = {"id": grp['id'], "name": name}

      return applied_filter
    except:
      abort(404, message="Error creating filter on server")
    

@blp.route("/filter/<string:filter_id>/cohort-analysis")
class CohortAnalysisService(MethodView):
  '''performs analysis for the cohort.  This anlysis includes
    creating a network
    performing autogrouping
    creating comparisons
  '''
  def get(self, filter_id):
    src = user['connection'].get_source(name=user['source_name'])
    grp = src.get_group(id=filter_id)

    # note: is group not found returns {'msg': 'Group with given parameter does not exist'}
    # if found it returns the group dict
    if "id" not in grp.keys():
      abort(404, message=f"Unable to find filter {filter_id} on platform")
    else:
      #create the network
      #TODO - OAA with Target?  Or using metric and lense from base network
      #Discussion with Amy recommended using the same metric and lense that she used in her analysis
      #check to see if network exists
      nw = src.get_network(grp['name'])
      if type(nw) == dict: 
        network = src.create_network(grp['name'],{
                      'row_group_id': grp['id'],
                      'column_set_id': src.get_column_set(name='features')['id'],  #TODO - get column set from correct base network
                      'metric': {'id': 'Angle'},
                      'lenses': [{'resolution': 30, 'id': 'Metric PCA coord 1',
                                  'equalize': True, 'gain': 3.0},
                                {'resolution': 30, 'id': 'Metric PCA coord 2',
                                  'equalize': True, 'gain': 3.0}]
                        }
                      )
        
        #TODO - Change from hard coded target to env or passed as param
        coloring_values = network.get_coloring_values(name='SpeciesColor')

        autogroups = network.autogroup_create(algorithm='AHCL', 
                                            coloring_values=coloring_values,
                                            cutoff_strength=0.75, 
                                            min_node_count=3,
                                            name=grp['id'])

        #create comparisons vs rest
        for g in autogroups.groups:
          src.compare_groups(group_1_name=g['name'],group_2_name="Rest", async_=False)

    return {"message": "cohort analysis complete"}
    