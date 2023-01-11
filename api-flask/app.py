import os
import sys  

import ayasdi.core as ac
from flask import Flask
from flask_smorest import Api

from dotenv import load_dotenv
from resources.status import blp as StatusBlueprint
from resources.graph import blp as GraphBlueprint
from resources.kpi import blp as KpiBlueprint
from resources.filter import blp as FilterBlueprint
from resources.explain import blp as ExplainBlueprint
from resources.group import blp as GroupBlueprint
from resources.patient import blp as PatientBlueprint

from globals import user

print(user)

load_dotenv()
user['name'] = os.getenv('EUREKA_USER')
user['password'] = os.getenv('EUREKA_PASS')
user['api_url'] = os.getenv('AYASDI_APISERVER')
user['source_name'] = os.getenv('SOURCE_NAME')
user['source_name_holdout'] = os.getenv('SOURCE_NAME_HOLDOUT')

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
    print('**** checking login ****') 
    try:
        result = user['connection'].check_platform_version()
        print("**** user already connected ****")
    except:
        print("**** user not logged in, loggin in now ****")
        connection = ac.Api(username=user['name'], password=user['password'], url=user['api_url'], ignore_version=True)
        user['connection'] = connection
        print("**** User Connected:", connection.is_connected, '****')

@app.get("/test")
def get_test():
    return {"message": "The test worked!"}

@app.get("/cookies")
def get_cookie():

    try:
        user['connection'].session.cookies.clear()
        user['connection'].check_platform_version()
        return {"message": "Error reseting cookie !"}

    except:
        return {"message": "Cookie was reset"}


api.register_blueprint(StatusBlueprint)
api.register_blueprint(GraphBlueprint)
api.register_blueprint(KpiBlueprint)
api.register_blueprint(FilterBlueprint)
api.register_blueprint(ExplainBlueprint)
api.register_blueprint(GroupBlueprint)
api.register_blueprint(PatientBlueprint)



