import qrcode
import hashlib
import os


def generate_hash_key(row, features_selected):
    # initialize hash_key as empty string
    hash_key = ""
    # concatenate values from given features to generate hash_key
    for feature in features_selected:
        print(feature)
        hash_key += str(row[feature]) + ""
    hash_key = hashlib.sha256(hash_key.encode()).hexdigest()
    # return hash_key
    return hash_key

# Link for website
def create_qr_code(obj, date):
        #features_selected = ["batch_no","MK_number","sample_number"]
        #unique_hash = generate_hash_key(row, features_selected)
       
        protein_concentration = obj['protein_concentration']
        batch_id = obj['batch_id']
        sample_id = obj['sample_id']
        
        #Implement nareen and yuki's hashing
        unique_hash = f"{sample_id[0:3]}-{batch_id[0:3]}-{protein_concentration[0:3]}"
        unique_hash = str(unique_hash)
        
        #Creating an instance of qrcode
        obj = {
                "qr_code_key": f"{unique_hash}",
                "date_entered": f"{date}",
        }

        qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5)
        qr.add_data(obj)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        qr_code_dir = os.path.join(os.getcwd(),'backend','qr_codes')
        img.save(f'{qr_code_dir}/{unique_hash}.png')
        return unique_hash

