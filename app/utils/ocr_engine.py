# import easyocr
# from PIL import Image
# import io

# reader = easyocr.Reader(['en'], gpu=False)

# def perform_easyocr(image_file):
#     contents = image_file.file.read()
#     image = Image.open(io.BytesIO(contents))
#     result = reader.readtext(contents, detail=0)
#     return ' '.join(result)

import easyocr
from PIL import Image
import io

reader = easyocr.Reader(['en'], gpu=False)

def perform_easyocr(image_file):
    contents = image_file.file.read()
    image = Image.open(io.BytesIO(contents))
    result = reader.readtext(contents, detail=0)
    
    extracted = ' '.join(result)
    print("🧾 OCR Extracted:", extracted)  # 👈 ADD THIS
    return extracted
