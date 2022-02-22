# Merck-label-dashboard


## How to run the project

### DOCKER METHOD
#### WARNING: BEFORE DOING THIS MAKE SURE YOU HAVE DOCKER DESKTOP and Docker-compose CLI INSTALLED ON LOCAL DEVICE
1. `cd frontend` to CD into frontend directory and run `npm install` or `npm i`.
2. `cd ../` to return back to main project directory.
3. Simply run this command in parent directory `docker-compose up && docker-compose rm -fsv`



### TROUBLE-SHOOTING
#### 1. (MAC) If port 5000 is used.
If you are using a mac and when you try to run the docker-compose command and it says that port 5000 is used; chances are that airplay is using port 5000. 

FIX:
- https://nono.ma/port-5000-used-by-control-center-in-macos
- `You can deactivate AirPlay Receiver in System Preferences › Sharing, and unchecking AirPlay Receiver to release port 5000.`

#### 2. Can't run react script.
This is most likely the case with missing node modules when you first clone this repository, so a potential solution would be to `npm install` to install the node modules.

FIX:
- You might have to cd into the frontend directory and type in the terminal `npm install` to install the node modules.
