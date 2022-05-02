API endpoints
===============

1. ``/scan/qr_code``
------------------------
This api endpoint is used for retrieving the information from the database using the qr_code_key.
    - Method:
        POST
    - Parameters:
         qr_code_key:
            Key that is stored in the qr_code that was scanned by the frontend
    
    - Returns:
        - JSON with information retrieved from the database.

2. ``/create/qr_code``
--------------------------
This api endpoint is used for creating a new label and qr_code for the newly inputted sample.
    - Method:
        POST
    - Parameters:
         JSON with fields:
            - analyst
            - experiment_id
            - storage_condition
            - date_entered
            - contents
            - size
    
    - Returns:
        - qr_code_key:
            Newly generated qr_code_key with information inputted.

3. ``/assets/qr_code/<qr_code_key>``
--------------------------------------
This api endpoint is used for querying the database to get the image of the label using the qr_code_key.
    - Method:
        GET
    - URL Parameters:
        - qr_code_key:
            label image that you want to retrieve from the server.
    
    - Returns:
        - Label image:
            the image of the created label in .png format.

4. ``/csv``
--------------------------------------
This api endpoint is used for when the user wants to dump a csv file to our backend so that it gets parsed and stored into our database. 

This api_endpoint checks if an entry exists, if not it hashes a new qr_code_key, else it updates the existing fields associated to the entry.
    - Method:
        POST
    - URL Parameters:
        - CSV file:
            | CSV that was sent from the frontend. 
            | Note that the CSV should have the following columns:
                - analyst
                - experiment_id
                - storage_condition
                - date_entered
                - contents
    
    - Returns:
        - String:
            ``"Total Entries:{values[0]+values[1]} New:{values[0]} Updated:{values[1]}"``:
                - Total entires: Total amount of columns in .csv file
                - New: New entries that were not previously in the database.
                - Updated: Entries with existing qr_code_keys that were updated by the new entries from the csv.
