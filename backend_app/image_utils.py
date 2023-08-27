# backend_app/image_utils.py
from PIL import Image
from io import BytesIO

def process_image(image):
    try:
        # 读取文件的二进制数据
        image_content = image.read()

        # 尝试打开图像
        try:
            img = Image.open(BytesIO(image_content))
        except Exception as e:
            print(f"Error opening image: {e}")
            return None

        # 尝试进行图像处理
        try:
            gray_img = img.convert('L')
            print(f"process sucessed image: {gray_img}")
            return gray_img
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    except Exception as e:
        print(f"Error reading image content: {e}")
        return None
