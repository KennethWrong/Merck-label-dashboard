Troubleshooting
=================

1. (MAC) If port 5000 is used
-------------------------------
If you are using a mac and when you try to run the docker-compose command and it says that port 5000 is used; 
chances are that airplay is using port 5000.

Fix:
https://nono.ma/port-5000-used-by-control-center-in-macos
.. code-block:: console

   You can deactivate AirPlay Receiver in System Preferences › Sharing, and unchecking AirPlay Receiver to release port 5000.

2. Can't run react script
-------------------------------
This is most likely the case with missing node modules when you first clone this repository, so a potential solution would be to npm install to install the node modules.

Fix:
CD to the frontend directory:
.. code-block:: console

   $ cd frontend

Install all the node dependencies:
.. code-block:: console

   $ npm install

3. Failed to execute script docker-compose
---------------------------------------------
This is most likely due to the fact that your docker desktop is not running.

Fix:
Open your docker desktop and keep it running.

4. Database not connecting with backend
-----------------------------------------
This is most likely due to the fact that you do not have the .env file in your backend directory.

Fix:
Ask your project manager for the .env file and place it into your backend directory.

5. Fonts are off
-----------------------------------------
The website looks complete off and everything is misplaced.

Fix:
Try changing to ``google chrome`` as this application is best used on google chrome.