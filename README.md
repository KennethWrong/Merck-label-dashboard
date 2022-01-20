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
1. CD to the backend folder.
2. Run the command `pip install -r requirements.txt` to download the dependencies and their respective versions
3. CD ../ back to merck directory
4. FOR MAC: Run the command `python3 app.py` to start the flask server.
5. FOR WINDOWS: Run the command `python app.py` to start the flask server.
6. The backend will be running on localhost:5000

### Connecting frontend and backend
1. To make calls from the front-end to backend we will be making http calls to  `http://localhost:5000/<api-endpoint>`

### Test with just backend serving front-end pages
1. As of right now we are separating front-end and backend. To combine the two you would do the following.
2. CD to frontend
3. `npm run build`
4. Uncomment code in app.py that says for deployment
5. run app.py file and go to localhost:5000
**NOTE: When deploying like this, changes in the front-end will not show**

## Future Plans
- Temporarily using SQLite as a relational database until we get access to AWS PostGreSQL.
- Will also add ability to batch dump .csv files into S3 Bucket.
- Containerize and scale web application with docker, k8.

## Phase 1 of Website
<img width="741" alt="Screen Shot 2021-11-22 at 11 34 17 AM" src="https://user-images.githubusercontent.com/70383225/142899733-6c013787-0480-4e1c-81a6-9ed78eebccb3.png">

