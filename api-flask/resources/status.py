from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from globals import user, get_all_group_id

blp = Blueprint("status", __name__, description="Operations on status")

@blp.route("/status")
class StatusService(MethodView):
  def get(self):
    print('in status')
    return {'is_connected': user['connection'].is_connected, 'eureka_user': user['name'], 'eureka_url': user['api_url']}
