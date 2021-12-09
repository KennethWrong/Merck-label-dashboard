import qrcode
import sys

# Link for website
def create_qr_code(obj, date):

        protein_concentration = obj['protein_concentration']
        batch_id = obj['batch_id']
        sample_id = obj['sample_id']
        
        #Implement nareen and yuki's hashing
        unique_hash = hash(sample_id+batch_id + protein_concentration)
        unique_hash = str(abs(unique_hash))[0:10]
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
        img.save(f'/Users/werunm/Desktop/Merck-label-dashboard/backend/qr_codes/{unique_hash}.png')
        return unique_hash

