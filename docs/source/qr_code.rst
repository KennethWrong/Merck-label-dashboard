qr_code
===============

1. join_directories
------------------------
.. py:function:: qr_code.join_directories(*paths)

   A helper function to generate the absolute path and joining multiple paths together.

   :param paths: args of strings of path.
   :type paths: args of strings
   :return: return absolute path in string
   :rtype: string

2. generate_hash_key
-----------------------
.. py:function:: qr_code.generate_hash_key(row, features_selected)

   To generate a hash key as a primary key for the entries of the samples in our DB.

   :param row: Status code to return to frontend.
   :type row: int or ``200``
   :param features_selected: a list that is ['experiment_id', 'storage_condition', 'analyst','contents','date_entered','expiration_date']
   :type features_selected: list
   :return: qr_code_key : Returns generated hashed qr_code_key
   :rtype: str

3. test_fit_using_ttf_font
-----------------------------
.. py:function:: qr_code.test_fit_using_ttf_font(font_size, string, font_filename, available_width)

   Adjust font size to fit available white space instead of overlapping the qr code.

   :param font_size: font size that we choose to use.
   :type font_size: str
   :param string: String that we want to print onto the label.
   :type string: str
   :param font_file: name of the font file.
   :type font_file: str
   :param available_width: width for adjusting text.
   :type available_width: str
   :return: font: The updated ttf font.
   :rtype: ImageFont.truetype
   :return: font_size: size of the font.
   :rtype: int

4. anchor_adjustment
------------------------
.. py:function:: qr_code.anchor_adjustment(desired_location, string, font)

   Adjust text location using middle bottom to text location using left upper.

   :param desired_location: The text location using middle bottom part of text.
   :type desired_location: str
   :param string: The text that will be used to be placed onto the label.
   :type string: str
   :param font: ttf font object
   :type font: ImageFont.truetype
   :return: left_location
   :rtype: str

5. small_format
------------------------
.. py:function:: qr_code.small_format(qr_img, obj, font_filename, background_filename)

   Accept the qr code image and info from obj to generate a label suitable for 2ml and 2.5 ml vile

   :param qr_img: qr code generated in create_qr_code function.
   :type qr_img: img
   :param obj: Info contains columns in feature_selected.
   :type obj: dic
   :param font_filename: The name of the fontfile.
   :type font_filename: str
   :param background_filename: The name of the background filename.
   :type background_filename: str
   :return: img: a designed label image with text and qr code.
   :rtype: ImageFont.truetype

6. large_format
------------------------
.. py:function:: qr_code.large_format(qr_img, obj, font_filename, background_filename)

   Accept the qr code image and info from obj to generate a label suitable for 4ml and 10 ml vile

   :param qr_img: qr code generated in create_qr_code function.
   :type qr_img: img
   :param obj: Info contains columns in feature_selected.
   :type obj: dic
   :param font_filename: The name of the fontfile.
   :type font_filename: str
   :param background_filename: The name of the background filename.
   :type background_filename: str
   :return: img: a designed label image with text and qr code.
   :rtype: ImageFont.truetype

7. create_qr_code
------------------------
.. py:function:: qr_code.create_qr_code(obj)

   Creates a unique qr_code_key using arguments from obj, then uses qrcode library to generate a QR code containing the date and the qr_code key  

   :param obj: Dictionary with key value pairs of the fields of the sample: (experiment_id ,storage_condition, analyst, expiration_date, date_entered, contents)
   :type obj: dic
   :return: hash : Unique qr_code_key hash that is generated.
   :rtype: str