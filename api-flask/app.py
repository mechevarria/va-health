import os

import ayasdi.core as ac
from flask import Flask
from flask_restful import Api, Resource
from dotenv import load_dotenv
from status import StatusService
from graph import GraphService

load_dotenv()

eureka_user = os.getenv('EUREKA_USER')
eureka_pass = os.getenv('EUREKA_PASS')
eureka_url = os.getenv('AYASDI_APISERVER')

print(f'{eureka_user} is connecting to {eureka_url}')
# The Ayasdi Api needs to be namespaced to prevent a conflict with the Flask Api
conn = ac.Api(username=eureka_user, password=eureka_pass, url=eureka_url)

app = Flask(__name__)

api = Api(app)


class Status(Resource):
  service = StatusService(conn, eureka_user, eureka_url)
  def get(self):
    return self.service.get()

class Graph(Resource):
  service = GraphService()
  def get(self):
    return self.service.get()

api.add_resource(Status, '/status')
api.add_resource(Graph, '/graph')

if __name__ == '__main__':
    app.run(debug=True)
