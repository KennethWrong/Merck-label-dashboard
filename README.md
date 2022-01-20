# Merck-label-dashboard


## How to run the project

### UPDATED METHOD
#### WARNING: ONLY TESTED FOR MAC
1. IF YOU DON'T HAVE THE DEPENDENCIES: `run the command bash ./scripts/install.sh `
2. IF YOU HAVE THE DEPENDENCIES: `run the command bash ./scripts/dev.sh`

### OLD METHOD

### Frontend
1. CD into frontend 
2. Run command `npm install` to install dependencies and react packages.
3. Then run command `npm run start` to start up the front-end 
4. Frontend will be running on localhost:3000

### Backend
1. Run the command `pip install -r requirements.txt`
4. FOR MAC: Run the command `python3 ./backend/app.py` to start the flask server.
5. FOR WINDOWS: Run the command `python ./backend/app.py` to start the flask server.
6. The backend will be running on localhost:5000

### Connecting frontend and backend
1. To make calls from the front-end to backend we will be making http calls to  `http://localhost:5000/<api-endpoint>`

## Future Plans
- Temporarily using SQLite as a relational database until we get access to AWS PostGreSQL.
- Will also add ability to batch dump .csv files into S3 Bucket.
- Containerize and scale web application with docker, k8.


