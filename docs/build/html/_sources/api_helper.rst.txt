api_helper
===============

1. create_response
------------------------
.. py:function:: api_helper.create_response(message='',status_code=200, mimetype='application/json')

   A helper function to create response objects to send back to the frontend.

   :param message: Optional message to send back to the frontend.
   :type message: str or ``''``
   :param status_code: Status code to return to frontend.
   :type status_code: int or ``200``
   :param mimetype: Optional mimetype that defaults to type JSON.
   :type mimetype: ``'application/json'`` or other mime type.
   :return: Response object to send to send to frontend
   :rtype: flask.response

2. create_response_from_scannning
------------------------------------
.. py:function:: api_helper.create_response_from_scanning(message="", status_code=200, mimetype='application/json')

   A helper function to create response objects to send back to the frontend.

   :param message: Optional object payload to send back to the frontend.
   :type message: dic or ``''``
   :param status_code: Status code to return to frontend.
   :type status_code: int or ``200``
   :param mimetype: Optional mimetype that defaults to type JSON.
   :type mimetype: ``'application/json'`` or other mime type.
   :return: Response object to send to the frontend
   :rtype: flask.response

3. insert_new_sample
------------------------
.. py:function:: api_helper.insert_new_sample(qr_code_key,sample_obj)

   Inserts newly retrieved sample (both from CSV and input form) into our data base. Currently it overrites existing data.

   :param qr_code_key: The unique identifier for each sample entry.
   :type qr_code_key: str
   :param sample_obj: JSON containing sample information with structure of db schema.
   :type sample_obj: dic
   :return: Boolean to indicate whether or not inserting sample already existed. True if not. False if existed.
   :rtype: bool

4. parse_csv_to_db
------------------------
.. py:function:: api_helper.parse_csv_to_db(file_path,info)

   This function is called to parse a CSV uploaded and insert each column of the CSV into our DB.

   :param file_path: absolute path to our csv file.
   :type file_path: str
   :param info: [0,0], a list of size 2 with two intergers. info[0] is count of new samples inserted. info[1] is count of existing samples updated.
   :type file_path: list
   :return: Status-Code: 200 if successful, 500 if unsuccessful
   :rtype: int
