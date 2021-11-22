# Merck-lable-dashboard


## How to run the project
You would have to run the backend and frontend in two different terminal tabs.

### Frontend
1. CD into frontend and do npm install do install all dependencies and react packages.
2. Then do npm run start to start up the front-end 
3. Frontend will be running on port:3000

### Backend
1. Simply run the app.py folder in the backend folder to start the flask server.
2. The backend will be running on port:5000

### Connecting frontend and backend
1. To make calls from the front-end to backend we will be making http calls to  `http://localhost:5000/<api-endpoint>`

### Test with just backend serving front-end pages
1. As of right now we are separating front-end and backend. To combine the two you would do the following.
2. CD to frontend
3. `npm run build`
4. Uncomment code in app.py that says for deployment
5. run app.py file and go to localhost:5000
**NOTE: When deploying like this, changes in the front-end will not show**
## Phase 1 of Website
<img width="741" alt="Screen Shot 2021-11-22 at 11 34 17 AM" src="https://user-images.githubusercontent.com/70383225/142899733-6c013787-0480-4e1c-81a6-9ed78eebccb3.png">
- Temporarily using SQLite as a relational database until we get access to AWS RedShift
- Will implement csv parsing and table lookup
- Will also add ability to batch dump .csv files into S3 Bucket
