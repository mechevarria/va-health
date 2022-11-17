# VA Health
Master application for a REST api to the Eureka SDK and Vue.js based frontend

## api-flask
* Install required libraries
```bash
pip install ayasdi-sdk-3.0.0.7.tar.gz
conda install python-dotenv
conda install Flask
conda install Flask-RESTful
```
* Set necessary environment variables in `api-flask/.env`
```properties
EUREKA_USER="firstname.lastname@symphonyai.com"
EUREKA_PASS="my_password"
AYASDI_APISERVER="http://platform.ayasdi.com/workbench/"
```