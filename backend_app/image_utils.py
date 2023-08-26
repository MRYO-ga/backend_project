# backend_app/image_utils.py
from PIL import Image
from io import BytesIO
import tempfile

def process_image(image):
    image_content = image.read()
    img = Image.open(BytesIO(image_content))
    gray_img = img.convert('L')
    return gray_img
