from PIL import Image
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send, discover
from brother_ql.raster import BrotherQLRaster
import os

def print_image(image_obj):
    im = image_obj.resize((306, 991)) 

    backend = 'pyusb'    # 'pyusb', 'linux_kernal', 'network'
    model = 'QL-820NWB' # your printer model.
    printer = discover('pyusb')[0]['identifier'][:-2]

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    instructions = convert(
            qlr=qlr, 
            images=[im],    #  Takes a list of file names or PIL objects.
            label='29x90', 
            rotate='0',    # 'Auto', '0', '90', '270'
            threshold=70.0,    # Black and white threshold in percent.
            dither=False, 
            compress=False, 
            red=False,    # Only True if using Red/Black 62 mm label tape.
            dpi_600=False, 
            hq=True,    # False for low quality.
            cut=True
    )

    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

    return 200
