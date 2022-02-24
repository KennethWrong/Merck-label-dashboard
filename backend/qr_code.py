import qrcode
import hashlib
import os
from PIL import Image, ImageDraw,ImageFont
import functools
import sys
from db_helper import get_strf_utc_date

def join_directories(*paths):
        curr_dir = os.getcwd()
        paths = [curr_dir] + list(paths)
        destination_dir = functools.reduce(os.path.join,paths)
        return destination_dir+'/'


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
    # initialize hash_key as empty string
    hash_key = ""
    # concatenate values from given features to generate hash_key
    for feature in features_selected:
        hash_key += str(row[feature]) + ""
    hash_key = hashlib.sha256(hash_key.encode()).hexdigest()
    # return hash_key
    return hash_key[:10]

############################################################
# Function_name: generate_hash_key
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

def large_format(qr_img,obj):
    # place qr code image on background
    path = join_directories('files_for_label')
    # get a background white image for label
    img = Image.open(path + "white_image.jpeg")
    # resize it to a label size suitable for QR printer
    img = img.resize((696, 250))
    # resize the qr image to put on the background
    qr_img = qr_img.resize((230, 230))
    img.paste(qr_img, (450, 15))

    # Add text information
    draw = ImageDraw.Draw(img)
    fnt1 = ImageFont.load_default()
    fnt2 = ImageFont.load_default()
    fnt3 = ImageFont.load_default()

#     temperature, PH = obj["storage_condition"].split(", ")
#     concentration, contents = obj["contents"].split(", ")
    left_align = 40
#     msg1 = temperature + ", " + concentration + ", " + PH
    msg1 = obj["storage_condition"]
#     msg2 = "Prep " + str(obj["date_entered"]) + " " * 4 + "Expiry " + str(obj["expiration_date"])
    msg2 = obj["contents"]
    msg3 = "Prep By: " + obj["analyst"]
    draw.text((left_align, 55), obj["experiment_id"], font=fnt1, stroke_width=1, anchor="ls", fill=0)
    draw.text((left_align, 90), 'This is a placeholder for now', font=fnt1, anchor="ls", fill=0)
    draw.text((left_align, 130), msg1, font=fnt2, anchor="ls", fill=0)
    draw.text((left_align, 190), msg2, font=fnt3, anchor="ls", fill=0)
    draw.text((left_align, 220), msg3, font=fnt3, anchor="ls", fill=0)

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
#        'experiment_id':"5010613001301" ,
#        'storage_condition': "50C, pH 6.8",
#        'analyst': "AKPM",
#        'contents': "10 mM, potassium phosphate buffer",
#        'date_entered': "06Jan2022",
#        'expiration_date': "09Jan2022",
#        'date_modified': "12Feb2022"
#    }
#    - date : date of upload 
# Return:
#    - qr_code_key : Returns generated hashed qr_code_key
############################################################
def create_qr_code(obj):
        size = obj['size']
        #Modified hash key (need to improve with order-carefree)
        features_selected = ['experiment_id', 'storage_condition', 'analyst','contents']
        #Check if we got a null

        #Check if date_entered is already provided to us
        if 'date_entered' not in obj:
                obj['date_entered'] = get_strf_utc_date()

        #Check if field is empty
        if not obj['analyst'] or not obj['experiment_id']:
                return None
        
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
        #This will change according to the size
        if size == '2mL':
                pass #To be entered
        elif size == '2.5mL':
                pass #To be entered
        elif size == '4mL':
                img = large_format(qr_img, obj)
        elif size == '20mL':
                img = large_format(qr_img, obj)

        #Temporarily saves QR code into /qr_codes folder
        #Will be improved as we do not need to store it as we will send the QR code to the printer
        img.save(f'{qr_code_dir}/{unique_hash}.png')
        img.save(os.path.join(image_dir,'label.png')) ## need to modify the filename
        return unique_hash

