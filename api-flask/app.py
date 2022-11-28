import os

import ayasdi.core as ac
from flask import Flask
from flask_smorest import Api

# from flask_restful import Api, Resource
from dotenv import load_dotenv
from resources.status import blp as StatusBlueprint
from resources.graph import blp as GraphBlueprint
# from resources.graph import GraphService

from db import user

print(user)

load_dotenv()
user['name'] = os.getenv('EUREKA_USER')
user['password'] = os.getenv('EUREKA_PASS')
user['api_url'] = os.getenv('AYASDI_APISERVER')


print(f'{user["name"]} is connecting to {user["api_url"] }')
# The Ayasdi Api needs to be namespaced to prevent a conflict with the Flask Api
user['connection']  = ac.Api(username=user['name'], password=user['password'], url=user['api_url'])

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["API_TITLE"] = "VA-Health REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

@app.before_request 
def before_request_callback():
    print('checking login') 
    try:
        result = user['connection'].check_platform_version()
    except:
        print("user not logged in, loggin in now")
        connection = ac.Api(username=user['name'], password=user['password'], url=user['api_url'])
        print("User Connected:", connection.is_connected)



# class Graph(Resource):
#   service = GraphService()
#   def get(self):
#     return self.service.get()

api.register_blueprint(StatusBlueprint)
api.register_blueprint(GraphBlueprint)

# api.add_resource(Status, '/status')
# api.add_resource(Graph, '/graph')

