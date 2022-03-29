import qrcode
import hashlib
import os
from PIL import Image, ImageDraw,ImageFont
import functools
import sys
from db_helper import get_strf_utc_date
import zlib

def join_directories(*paths):
        curr_dir = os.getcwd()
        paths = [curr_dir] + list(paths)
        destination_dir = functools.reduce(os.path.join,paths)
        return destination_dir+'/'

def anchor_adjustment(desired_location,string,draw): # find location for "la" given "ms"
    text_width, text_height = draw.textsize(string, font=ImageFont.load_default())
    left_location = (desired_location[0] - text_width / 2, desired_location[1] - text_height)
    return left_location



############################################################
# Function_name: generate_hash_key
#
# Function_logic:
# To generate a hash key as a primary key for the entries of the samples in our DB
# 
#
# Arguments: 
#    - row : info contains columns in feature_selected
#    - features_selected: a list that is ['experiment_id', 'storage_condition', 
#                       'analyst','contents','date_entered','expiration_date']
    
# Return:
#    - qr_code_key : Returns generated hashed qr_code_key
############################################################
def generate_hash_key(row, features_selected):
    try:
        # initialize hash_key as empty string
        hash_key = ""
        # concatenate values from given features to generate hash_key
        for feature in features_selected:
                hash_key += str(row[feature]) + ""
        #hash_key = hashlib.sha256(hash_key.encode()).hexdigest()
        hash_key = hex(zlib.crc32(hash_key.encode()))[2:] # new hash key - only 8 digits
        # return hash_key
        return hash_key[:10]
    except Exception as e:
        print('Something went wrong when trying to generate a unique hash qr_code_key')
        print(e)

############################################################
# Function_name: test_fit_using_ttf_font
#
# Function_logic:
# Adjust font size to fit available white space instead of overlapping the qr code
# 
#
# Arguments: 
#    - font_size: font size
#    - string: adjusting text
#    - font_file: font filename
#    - available_width: adjusting text

    
# Return:
#    - font : updated ttf font
#    - font size: newly update font size
############################################################
def test_fit_using_ttf_font(font_size, string, font_filename, available_width):
    font = ImageFont.truetype(font_filename, font_size)
    text_width, text_height = font.getsize(string)
    while not (text_width <= available_width):
        font_size -= 1
        font = ImageFont.truetype(font_filename, font_size)
        text_width, text_height = font.getsize(string)
        #print(f"font mask= {font.getmask(string).getbbox()}")

    return ImageFont.truetype(font_filename, font_size), font_size
############################################################
# Function_name: anchor_adjustment
#
# Function_logic:
# adjust text location using middle bottom to text location using left upper
# 
#
# Arguments: 
#    - desired_location : the text location using middle bottom part of text
#    - string: the adjusting text
#    - font: ttf font
    
# Return:
#    - left_location : the text location using left upper
############################################################
def anchor_adjustment(desired_location, string, font): # find location for "la" given "ms"
    text_width, text_height = font.getsize(string)
    left_location = (desired_location[0] - text_width / 2, desired_location[1] - text_height)
    return left_location


############################################################
# Function_name: small_format
#
# Function_logic:
# accept the qr code image and info from obj to generate a label 
#       suitable for 2ml and 2.5 ml vile
#
# Arguments: 
#    - qr_img: qr code generated in create_qr_code function
#    - obj: info contains columns in feature_selected
    
# Return:
#    - img: a designed label image with text and qr code
############################################################
def small_format(qr_img, obj, font_filename, background_filename):
    try:
        # setup values
        size_l = (696, 223)  # size of the large label
        qr_margin = 40  # the pixel distance between right border of qr code and the right border of white background
        qr_size = (size_l[1] - 2 * qr_margin, size_l[1] - 2 * qr_margin)
        qr_location = (size_l[0] - qr_size[0] - int(qr_margin/4), qr_margin)  # where the left upper corner of qr code is

        # get a background white image for label
        img = Image.open(background_filename)
        # resize it to a label size suitable for QR printer
        img = img.resize(size_l)
        # resize the qr image to put on the background
        qr_img = qr_img.resize(qr_size)
        img.paste(qr_img, qr_location)  # left upper corner coordinates

        draw = ImageDraw.Draw(img)

        # information needed
        experiment_id = obj["experiment_id"]
        condition = obj["storage_condition"]
        contents = obj["contents"]
        date_entered = obj["date_entered"]
        expiration_date = obj["expiration_date"]
        analyst = obj["analyst"]

        msg_num = 4
        fnt_sizes = [25, 25, 25, 25]
        fnts = []
        for i in range(msg_num):
            fnts.append(ImageFont.truetype(font_filename, fnt_sizes[i]))

        # formatting
        lines = []
        lines.append(str(experiment_id))  # line 1: font size = 30
        lines.append("Prep " + str(date_entered))  # line 2: font size = 25
        lines.append("Prep By: " + analyst)  # line 3: font size = 25
        lines.append("Stored at: " + storage_condition) # line 4: font size = 25

        left_align = 200 # the pixel distance between the left of the text and the left of the border of white background
        available_width = size_l[0]

        # adjust font size to fit the available width
        fnt1_new, fnt1_size = test_fit_using_ttf_font(fnt_sizes[0], lines[0], font_filename, available_width)
        fnt2_new, fnt2_size = test_fit_using_ttf_font(fnt_sizes[1], lines[1], font_filename, available_width)
        fnt3_new, fnt3_size = test_fit_using_ttf_font(fnt_sizes[2], lines[2], font_filename, available_width)
        fnt4_new, fnt4_size = test_fit_using_ttf_font(fnt_sizes[3], lines[3], font_filename, available_width)

        line_heights = [60, 100, 140, 180]
        # draw texts line by line on the white background
        draw.text((left_align, line_heights[0]), lines[0], font=fnt1_new, stroke_width = 1, anchor="ls", fill=0)
        draw.text((left_align, line_heights[1]), lines[1], font=fnt2_new, anchor="ls", fill=0)
        draw.text((left_align, line_heights[2]), lines[2], font=fnt3_new, anchor="ls", fill=0)
        draw.text((left_align, line_heights[3]), lines[3], font=fnt4_new, anchor="ls", fill=0)


        return img
    except Exception as e:
            print('Something went wrong when trying to create a small QR_CODE')
            print(e)

    return img

############################################################
# Function_name: large_format
#
# Function_logic:
# accept the qr code image and info from obj to generate a label 
#       suitable for 4ml and 20 ml vile
#
# Arguments: 
#    - qr_img: qr code generated in create_qr_code function
#    - obj: info contains columns in feature_selected
    
# Return:
#    - img: a designed label image with text and qr code
############################################################

def large_format(qr_img, obj, font_filename, background_filename):
    # setup values
    size_l = (696, 223) # size of the large label
    qr_margin = 40 # the pixel distance between right border of qr code and the right border of white background
    qr_size = (size_l[1]-2*qr_margin, size_l[1]-2*qr_margin)
    qr_location = (size_l[0]-qr_size[0]-qr_margin, qr_margin) # where the left upper corner of qr code is

    # get a background white image for label
    img = Image.open(background_filename)
    # resize it to a label size suitable for QR printer
    img = img.resize(size_l)
    # resize the qr image to put on the background
    qr_img = qr_img.resize(qr_size)
    img.paste(qr_img, qr_location) # left upper corner coordinates

    # Add text information
    msg_num = 4
    fnt_sizes = [40,40,40,40]
    fnts = []
    for i in range(msg_num):
        fnts.append(ImageFont.truetype(font_filename, fnt_sizes[i]))


    draw = ImageDraw.Draw(img)

    # information needed
    experiment_id = obj["experiment_id"]
    storage_condition = obj["storage_condition"]
    contents = obj["contents"]
    date_entered = obj["date_entered"]
    expiration_date = obj["expiration_date"]
    analyst = obj["analyst"]

    # formatting
    lines = []
    lines.append(str(experiment_id)) # line 1: font size = 30, stroke width = 1
    lines.append(str(contents)) # line 2: font size = 30

    lines.append("Prep " + str(date_entered) + " " * 4 + "Expiry " + str(expiration_date)) # line 4: font size = 25
    lines.append("Prep By: " + str(analyst) + " " * 5 + "Stored at: " + str(storage_condition)) # line 5: font size = 25

    left_align = 20  # the pixel distance between the left of the text and the left of the border of white background
    available_width = size_l[0] - qr_size[0] - qr_margin - left_align

    # adjust font size to fit the available width
    fnt1_new, fnt1_size = test_fit_using_ttf_font(fnt_sizes[0], lines[0], font_filename, available_width)
    fnt2_new, fnt2_size = test_fit_using_ttf_font(fnt_sizes[1], lines[1], font_filename, available_width)
    fnt3_new, fnt3_size = test_fit_using_ttf_font(fnt_sizes[2], lines[2], font_filename, available_width)
    fnt4_new, fnt4_size = test_fit_using_ttf_font(fnt_sizes[3], lines[3], font_filename, available_width)


    line_heights = [50, 90, 130, 170, 200]
    # draw texts line by line on the white background
    draw.text((left_align, line_heights[0]), lines[0], font=fnt1_new, stroke_width=1, anchor="ls", fill=0)
    draw.text((left_align, line_heights[1]), lines[1], font=fnt2_new, anchor="ls", fill=0)
    draw.text((left_align, line_heights[2]), lines[2], font=fnt3_new, anchor="ls", fill=0)
    draw.text((left_align, line_heights[3]), lines[3], font=fnt4_new, anchor="ls", fill=0)



    return img
############################################################
# Function_name: create_qr_code
#
# Function_logic:
# Creates a unique qr_code_key using arguments from obj, then uses qrcode library
# to generate a QR code containing the date and the qr_code key  
#
# Arguments: 
#       (example)
#    - obj = { 
#        'experiment_id':"NB-9999999-301-01" ,
#        'storage_condition': "50C, pH 6.8",
#        'contents': "10 mM, potassium phosphate buffer",
#        'analyst': "AKPM",
#        'date_entered': "10/24/2022",
#        'expiration_date': "01/28/2022",
#        'date_modified': "10/24/2022"
#    }
# Return:
#    - qr_code_key : Returns generated hashed qr_code_key
############################################################
def create_qr_code(obj):

        #Check if field is empty
        if not obj['analyst'] or not obj['experiment_id']:
                return None
        
        #Modified hash key (need to improve with order-carefree)
        features_selected = ['experiment_id', 'storage_condition', 'analyst','contents']

        #Check if date_entered is already provided to us
        obj['date_entered'] = obj.get('date_entered', get_strf_utc_date())
        size = obj.get('size','2mL')
        unique_hash = generate_hash_key(obj, features_selected) # a string
        
        #Creating an instance of qrcode
        obj_qrkey = {
                "qr_code_key": f"{unique_hash}",
                "date_entered": f"{obj['date_entered']}",
        }

        #Using the library to create the QR code
        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
        qr.add_data(obj_qrkey)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')

        qr_code_dir = join_directories('qr_codes')
        image_dir = join_directories('files_for_label')
        img = qr_img
        
        path = image_dir
        font_filename = os.path.join(image_dir,"reg.ttf")
        background_filename = os.path.join(image_dir,"white_image.jpeg")
        #This will change according to the size
        if size == '2mL':
            img = small_format(qr_img, obj, font_filename, background_filename)
        elif size == '2.5mL':
            img = small_format(qr_img, obj, font_filename, background_filename)
        elif size == '4mL':
            img = large_format(qr_img, obj, font_filename, background_filename)
        else: # 20mL
            img = large_format(qr_img, obj, font_filename, background_filename)
        
            

        #Temporarily saves QR code into /qr_codes folder
        #Will be improved as we do not need to store it as we will send the QR code to the printer
        qr_img.save(f'{qr_code_dir}/{unique_hash}.png')
        #img.save(os.path.join(image_dir,f'{unique_hash}_{size}.png')) ## need to modify the filename
        img.save(os.path.join(image_dir,f'{unique_hash}_{size}.png'))
        
        return unique_hash

