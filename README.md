# VA Health
Master application for a REST api to the Eureka SDK and Vue.js based frontend

## api-flask
* Install required libraries
```bash
cd api-flask
pip install ayasdi-sdk-3.0.0.7.tar.gz
conda install python-dotenv
conda install Flask
conda install Flask-RESTful
pip install flask-smorest
```
* Set necessary environment variables in `api-flask/.env`
```properties
EUREKA_USER="firstname.lastname@symphonyai.com"
EUREKA_PASS="my_password"
AYASDI_APISERVER="https://platform.ayasdi.com/workbench/"
SOURCE_NAME="iris.csv"
FLASK_APP="app.py"
FLASK_DEBUG="1"
```

## frontend-vue
Sample web application integrating bootstrap based coreui with [Vue](https://vuejs.org/). Initial scafold done with Vue CLI. The project can be deployed as a [docker](https://docs.docker.com/install/) container or pushed directly with a [buildpack](https://docs.cloudfoundry.org/buildpacks/nginx/index.html) to [Microsoft Azure](https://azure.microsoft.com/en-us/)

![screenshot](screenshots/screenshot.png)

## Integration and Links

* [Vue cli](https://cli.vuejs.org/) used to generate this project
* [Style Guide](https://vuejs.org/v2/style-guide/) for Vue. Attempting to follow as best as possible
* [CoreUI Bootstrap](https://coreui.io) theme
* [Bootstrap-Vue](https://bootstrap-vue.org/) components
* [Vue Router](https://router.vuejs.org/) for view management
* [Vuex](https://vuex.vuejs.org/) for state management
* [vue-mobile-detection](https://github.com/ajerez/vue-mobile-detection) for checking mobile state
* [axios](https://github.com/axios/axios) as http client
* [jsonplaceholder](https://jsonplaceholder.typicode.com/) for sample table data

## Project setup

* Install a [nodejs](https://nodejs.org/en/download/) runtime is installed (LTS)

```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

* The server will be running on [http://localhost:3000](http://localhost:3000)

### Compiles and minifies for production
```
npm run build
```

## Run as docker container

>You can create a public registry with security scanning for free at [Quay.io](https://quay.io)

* Build and push the image with this script. You will have to edit the quay.io registry endpoint for the push command to work
```bash
docker-frontend-build.sh
```

* Run the continer with this script
```bash
docker-frontend-run.sh
```

## Docker Import/Export

* Make sure the api and frontend images are built with the `api-flask/docker-api-build.sh` and `frontend-vue/docker-frontend-build.sh`

* Build the tar files with `docker-save.sh`

* Load the save file with `docker-load.sh`

* Run the containers with `docker-run-all.sh`
> Make sure there is a .env file with the environment variables for the api conatiner to read

* Stop the container with `docker-stop-all.sh`

## Testing api-flask in [Postman](https://www.postman.com/downloads/)

TODO

* Import the environment
* Import the collection

## Items 
### Frontend
* provide user friendly name for groups (g1, g2, etc).  This is only in UI so users can discuss easily and to improve look
* Individual Group Explains
    * Add scale values to boxplot
    * Question - Combine zero / one binary categorical explains into one? (note this should be done on backend)
    * Question - Sort explains by stastical importance? (note this should be done on backend)
* Add additional filter columns based on clinician feedback
### API
* Handle when cohort analysis fails
* Add color change endpoint that just gets colors?  Note: May be difficult without regen graph 
* Combine zero / one binary categorical explains into one
