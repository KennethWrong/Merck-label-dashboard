#!/bin/sh

#Installs requirements.txt
pip install -r requirements.txt

cd ./frontend
#Installing libraries and packages on the frontend
npm install
cd ../

#Running the dev.sh which runs our frontend code and backend code
bash ./scripts/dev.sh

