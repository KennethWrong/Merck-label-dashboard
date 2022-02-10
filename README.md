# Merck-label-dashboard


## How to run the project

### DOCKER METHOD
#### WARNING: BEFORE DOING THIS MAKE SURE YOU HAVE DOCKER DESKTOP and Docker-compose CLI INSTALLED ON LOCAL DEVICE
1. Simply run this command in parent directory `docker-compose up && docker-compose rm -fsv`

### Connecting frontend and backend
1. To make calls from the front-end to backend we will be making http calls to  `http://localhost:5000/<api-endpoint>`

## Future Plans
- Temporarily using SQLite as a relational database until we get access to AWS PostGreSQL.
- Will also add ability to batch dump .csv files into S3 Bucket.
- Containerize and scale web application with docker, k8.


