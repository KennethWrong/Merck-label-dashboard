#!/bin/sh

##Installing a node package that allows multiple terminal command execution
npm install ttab -g

##Kills port 3000 and 5000 in case they were occupied
npx kill-port 3000
npx kill-port 5000

#Creates a new tab in the same directory and runs our backend code
ttab -w python3 ./backend/app.py

#Runs our front-end code
/bin/sh -ec "cd frontend && npm run start"
