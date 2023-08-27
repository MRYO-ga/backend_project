# backend_app/tasks.py
from celery import shared_task
from .models import UserImage
from .image_utils import process_image
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render
# from time import sleep

@shared_task(retry_kwargs={'max_retries': 0})
def process_and_save_image(user_image_id):
    print("任务_1已运行！")
    try:
        user_image_model = UserImage.objects.get(id=user_image_id)
        processed_image = process_image(user_image_model.image)
        print("process image sucessed")
        buffer = BytesIO()
        processed_image.save(buffer, format='JPEG')
        print("save image file sucessed")
        # sleep(10)
        # print("sleep ok------")
        user_image_model.processed_image.save(user_image_model.image.name, ContentFile(buffer.getvalue()), save=True)
        print("save user image model sucessed")
        return user_image_model.id

    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return None

# process_image_complete 视图函数:该函数无效！！
# def process_image_complete(request, user_image_id):
#     user_image = UserImage.objects.get(id=user_image_id)
#     # 在这里处理任务完成后的操作，例如更新数据库或发送通知等
#     print(f"Image processing completed for UserImage {user_image_id}")
#     context = {
#         'uploaded_image_url': user_image.image.url,
#         'processed_image_url': user_image.processed_image.url  # 添加这一行
#     }
#     print("render image_display")
#     return render(request, 'image_display.html', context)

# process_image_callback 任务函数
@shared_task
def process_image_callback(result, *args, **kwargs):
    print("任务_3已运行！")
    # if result:
    #     user_image_id = result
    #     return process_image_complete(None, user_image_id)  # 返回视图函数的结果
