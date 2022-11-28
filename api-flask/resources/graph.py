from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import jsonify

from db import user

blp = Blueprint("graph", __name__, description="Operations on graph")

@blp.route("/graph")
class GraphService(MethodView):
  def get(self):
    data = [
            {'from': 'A', 'to': 'C'},
            {'from': 'A', 'to': 'D'},
            {'from': 'A', 'to': 'E'},
            {'from': 'A', 'to': 'F'},
            {'from': 'A', 'to': 'G'},
            {'from': 'B', 'to': 'C'},
            {'from': 'B', 'to': 'D'}
        ]
    return jsonify(data)

