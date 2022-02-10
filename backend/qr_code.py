import qrcode
import hashlib
import os

############################################################
# Function_name: generate_hash_key
#
# Function_logic:
# To generate a hash key as a primary key for the entries of the samples in our DB
# 
#
# Arguments: 
#    - row : ???
#    - features_selected: ???
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
# Function_name: create_qr_code
#
# Function_logic:
# Creates a unique qr_code_key using arguments from obj, then uses qrcode library
# to generate a QR code containing the date and the qr_code key  
#
# Arguments: 
#    - obj : {protein_concentration, batch_id, sample_id}
#    - date : date of upload 
# Return:
#    - qr_code_key : Returns generated hashed qr_code_key
############################################################
def create_qr_code(obj):
        
        #Modified hash key (need to improve with order-carefree)
        features_selected = ['analyst','experiment_id']
        unique_hash = generate_hash_key(obj, features_selected) # a string
        
        #Creating an instance of qrcode
        obj = {
                "qr_code_key": f"{unique_hash}",
                "date_entered": f"{obj['date_entered']}",
        }
        
        #Using the library to create the QR code
        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
        qr.add_data(obj)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        qr_code_dir = os.path.join(os.getcwd(),'qr_codes')

        #Temporarily saves QR code into /qr_codes folder
        #Will be improved as we do not need to store it as we will send the QR code to the printer
        img.save(f'{qr_code_dir}/{unique_hash}.png')
        return unique_hash

