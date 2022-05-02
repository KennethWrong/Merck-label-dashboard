db_helper
===============

1. insert_new_sample
------------------------
.. py:function:: db_helper.insert_new_sample(qr_code_key, sample_obj)

   This function is invoked after we have checked that the entry is unique to the db.

   :param qr_code_key: The unique identifier for each sample entry.
   :type qr_code_key: str
   :param sample_obj: Dictionary with key value pairs of the fields of the sample: (experiment_id ,storage_condition, analyst, expiration_date, date_entered, contents)
    
   :type sample_obj: dic
   :return: Response object to send to send to frontend
   :rtype: flask.response

2. update_sample_by_qr_code_key
------------------------------------
.. py:function:: db_helper.update_sample_by_qr_code_key(qr_code_key, sample_obj)

   These function is invoked when the user tries to create a new entry but an existing entry already exists.

   :param qr_code_key: The unique identifier for each sample entry.
   :type qr_code_key: str
   :param sample_obj:  Dictionary with key value pairs of the fields of the sample: (experiment_id ,storage_condition, analyst, expiration_date, date_entered, contents)
   :type sample_obj: dic
   :param mimetype: Optional mimetype that defaults to type JSON.
   :type mimetype: ``'application/json'`` or other mime type.
   :return: Response object to send to the frontend
   :rtype: flask.response

3. retrieve_sample_information_with_key
-----------------------------------------
.. py:function:: db_helper.retrieve_sample_information_with_key(qr_code_key)

   Retrieves from the database using the qr_code_key provided to us.

   :param qr_code_key: The unique identifier for each sample entry.
   :type qr_code_key: str
   :return: Tuple with row entry in database
   :rtype: tuple

4. check_if_key_exists
------------------------
.. py:function:: db_helper.check_if_key_exists(qr_code_key)

   Given the qr_code_key we check if a row with this key exists, if it does we return True, else we return False

   :param qr_code_key: The unique identifier for each sample entry.
   :type qr_code_key: str
   :return: Boolean. True if key exists. False if key does not exist.
   :rtype: bool

5. get_strf_utc_time
------------------------
.. py:function:: db_helper.get_strf_utc_date(input='')

   Creates a formatted string of the current utc time. If called with no parameters function will auto generate current utc date.

   :param input: The unique identifier for each sample entry.
   :type qr_code_key: datetime or ''
   :return: converted datetime to string with ``"%m/%d/%Y"`` format
   :rtype: string