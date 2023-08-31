# backend_app/image_utils.py
import cv2
import roop.globals
import roop.metadata
import roop.utilities as util
from roop.core import set_execution_provider
from roop.face_util import extract_face_images
from roop.capturer import get_image_frame

# def process_image(image):
#     try:
#         print(f"core.run() start----------")
#         core.run()
#         print(f"core.run() end----------")
#         # 读取文件的二进制数据
#         image_content = image.read()

#         # 尝试打开图像
#         try:
#             img = Image.open(BytesIO(image_content))
#         except Exception as e:
#             print(f"Error opening image: {e}")
#             return None

#         # 尝试进行图像处理
#         try:
#             gray_img = img.convert('L')
#             print(f"process sucessed image: {gray_img}")
#             return gray_img
#         except Exception as e:
#             print(f"Error processing image: {e}")
#             return None

#     except Exception as e:
#         print(f"Error reading image content: {e}")
#         return None


def process_image(src_image, dst_image):
    try:
        if src_image is None:
            print("Source image is missing.")
            return None

        if dst_image is None:
            print("Destination image is missing.")
            return None

        # update cfg data
        roop.globals.server_name = ""
        roop.globals.server_port = 0
        roop.globals.server_share = False
        roop.globals.output_image_format = 'png'
        # roop.globals.output_video_format = 'mp4'
        # roop.globals.output_video_codec = 'libx264'
        # roop.globals.video_quality = 14
        # roop.globals.live_cam_start_active = False
        roop.globals.max_threads = 4
        roop.globals.memory_limit = 0 # 限制运算最大内存
        roop.globals.frame_buffer_size = 4
        roop.globals.provider = 'cuda'
        roop.globals.force_cpu = False # 使用cpu分析人脸

        set_execution_provider(roop.globals.provider)
        print(f'Available providers {roop.globals.execution_providers}, using {roop.globals.execution_providers[0]} - Device:{util.get_device()}')

        roop.globals.INPUT_FACES.clear()
        roop.globals.TARGET_FACES.clear()
        SELECTION_FACES_DATA = None
        SELECTION_FACES_DATA = extract_face_images(src_image,  (False, 0))
        if SELECTION_FACES_DATA is None:
            print("No faces were detected in the source image.")
            return None
        roop.globals.INPUT_FACES.append(SELECTION_FACES_DATA[0][0])

        SELECTION_FACES_DATA = None
        SELECTION_FACES_DATA = extract_face_images(dst_image,  (False, 0))
        if SELECTION_FACES_DATA is None:
            print("No faces were detected in the source image.")
            return None
        roop.globals.TARGET_FACES.append(SELECTION_FACES_DATA[0][0])

        image_filename          = dst_image
        # bt_destfile             = "file_name"   # 目标文件
        select_face_index       = 0             # 输入图像人脸index
        selected_enhancer       = "GFPGAN"      # ["None", "Codeformer", "DMDNet", "GFPGAN"]
        selected_face_detection = "First found" # ["First found", "All faces", "Selected face", "All female", "All male"]
        max_face_distance       = 0.65          # 相似度：(0.01, 1.0), default value=0.65
        blend_ratio             = 0.65          # 融合程度：(0.0, 1.0), default value=0.65
        chk_useclip             = False         # 蒙版Mask：是否使用蒙版
        clip_txt                = ""            # 蒙版Mask：蒙版内容,placeholder="cup,hands,hair,banana

        previewinputs = [image_filename, select_face_index, selected_enhancer, selected_face_detection,
                        max_face_distance, blend_ratio, chk_useclip, clip_txt]
        
        return swap_faces(*previewinputs)
    except Exception as e:
        print(f"Error in process_image: {e}")
        return None

# 功能1：识别输入人脸

# 功能2：多人脸图像，从页面获取选择的人脸index，显示预览图像

# 功能3：交换人脸
def swap_faces(filename,
               select_face_index,
               enhancer,
               detection,
               face_distance,
               blend_ratio,
               use_clip,
               clip_text):
    from roop.core import live_swap
    current_frame = get_image_frame(filename)
    if current_frame is None:
        print("swap_faces input image is missing.")
        return None 

    roop.globals.face_swap_mode = translate_swap_mode(detection)
    roop.globals.selected_enhancer = enhancer
    roop.globals.distance_threshold = face_distance
    roop.globals.blend_ratio = blend_ratio

    if use_clip and clip_text is None or len(clip_text) < 1:
        use_clip = False

    roop.globals.execution_threads = roop.globals.max_threads
    current_frame = live_swap(current_frame, roop.globals.face_swap_mode, use_clip, clip_text, select_face_index)
    if current_frame is None:
        return None
    return current_frame


def translate_swap_mode(dropdown_text):
    if dropdown_text == "Selected face":
        return "selected"
    elif dropdown_text == "First found":
        return "first"
    elif dropdown_text == "All female":
        return "all_female"
    elif dropdown_text == "All male":
        return "all_male"
    
    return "all"

# Gradio wants Images in RGB
def convert_to_gradio(image):
    if image is None:
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
