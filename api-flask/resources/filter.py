from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify
from schemas import FilterSchema, AppliedFilter

from db import user

blp = Blueprint("filter", __name__, description="Operations on filters")

# @blp.route("/filter")
@blp.route("/filter")
class FilterService(MethodView):
  def generate_filter_name(self, filters):
    _name = []
    for filter in filters:
      if filter['categorical']:
        _name.append('_'.join([filter['name'], 'IS' if  filter['is_equal'] else 'isNOT', str(filter['value'])]))
      else:
        _name.append('_'.join([filter['name'], str(filter['min']), 'to', str(filter['max'])]))

    return '; '.join(_name)

  def generate_filter_dict(self, filters):
    _fds = []
    for filter in filters:
      if filter['categorical']:
        _fds.append({"column_name": filter["name"], "in_set": [filter['value']], "not": filter["is_equal"]})
      else:
        _fds.append({"column_name": filter["name"], "in_range": [filter["min"], filter["max"]]})

    return _fds

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

    name = self.generate_filter_name(filter_data)
    #check to see if filter has already been applied
    src = user['connection'].get_source(name=user['source_name'])
    grp = src.get_group(name=name)
    #note: is group not found returns {'msg': 'Group with given parameter does not exist'}
    #if found it returns the group dict
    if "id" in grp.keys():
      #group had been created before, just return id and name
      applied_filter = {"id": grp['id'], "name": name}
      return applied_filter
    else:
      #create a filter set
      fs = src.create_filter_set(self.generate_filter_dict(filter_data))
      #Create the groups from the filters
      grp = src.create_group(name=name, filter_set=fs)

      applied_filter = {"id": grp['id'], "name": name}
      return applied_filter
