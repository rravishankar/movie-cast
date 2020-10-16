#/bin/sh
source env/bin/activate
export FLASK_ENV=development
export FLASK_APP=app.py
export MOVIE_DB_USER="postgres" #DEPLOY_MODE=dev that is local database 
export MOVIE_DB_PASSWORD="postgres" #DEPLOY_MODE=dev that is local database 
export AUTH0_DOMAIN_NAME="" #From Auth0
export AUTH0_CLIENT_ID="" #From Auth0
export API_IDENTIFIER="" #From Auth0
export DEPLOY_MODE="prod" #"dev" is for development mode, else it's production. Used for database
export LOG_LEVEL="DEBUG" #Valid value is DEBUG else the logger logs INFO & above #TBD to be fixed to include all levels. Used in app.py
#TBD Repetitive need to be fixed in future release - check above variable names
export AUTH0_DOMAIN='' #From Auth0
export ALGORITHMS='' #From Auth0
export API_AUDIENCE='movie' #From Auth0
#JWT tokens for each of the roles Casting Asisstant, Casting Director and Executive Producer
export EXEC_PRODUCER_TOKEN=""
export CASTING_DIRECTOR_TOKEN=""
export CASTING_ASSISTANT_TOKEN=""
#Heroku Postgre Database URI
export DATABASE_URI=""
# export PORT=5000
