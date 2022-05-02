Usage
=====

IMPORTANT
----------
A important note is that you will need the secret .env file to make the project work.
You could get this .env file by the project manager.

Once you have gotten the .env file place it in the backend directory.

Another importance is that this application is built to run on Google Chrome. Attempts to run this on other web browsers may break the application.

Installation
------------
For mac:
In order to run the project you would first have to install docker desktop. Have it running on your local
machine. 

Open up a terminal in the project directory and CD into the front end:

.. code-block:: console

   $ cd frontend

Then install all dependencies using npm to create the node modules:

.. code-block:: console

   $ npm install

Then return back to the main directory:

.. code-block:: console

   $ cd ../

Then run the command:

.. code-block:: console

   $ docker-compose up && docker-compose rm -fsv
