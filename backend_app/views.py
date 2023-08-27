# backend_app/views.py
from django.shortcuts import render
from .forms import UploadImageForm
from .models import UserImage
from django.core.exceptions import ValidationError
from .tasks import process_and_save_image   # 引入新的任务
from .tasks import process_image_callback
import traceback
from celery.result import AsyncResult
from django.shortcuts import redirect

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            image = form.cleaned_data['image']

            try:
                user_image = UserImage(user_id=user_id, image=image)
                user_image.save()
                print("start process_and_save_image...")

                # 将图像处理任务添加到Celery队列中，设置回调函数
                # process_image_callback为视图函数，用于生成响应页面，而不是一个典型的 Celery 任务
                # 所以需要使用链式任务，process_and_save_image链接到另一个任务process_image_callback
                task = process_and_save_image.apply_async(args=[user_image.id], link=process_image_callback.s())

                # 重定向到 check_task_status 视图，并传递任务的 ID 作为参数
                return redirect('check_task_status', task_id=task.id)
            except Exception as e:
                error_message = f"An error occurred while processing the image: {e}"
                traceback.print_exc()
        else:
            error_message = "Invalid form submission. Please check the data."

        return render(request, 'upload_image.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadImageForm()
        return render(request, 'upload_image.html', {'form': form})

def check_task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.ready():
        if task.successful():
            result = task.result  # 获取任务结果
            if result is not None:
                user_image = UserImage.objects.get(id=result)
                context = {
                    'uploaded_image_url': user_image.image.url,
                    'processed_image_url': user_image.processed_image.url  # 添加这一行
                }
                return render(request, 'image_display.html', context)
            else:
                error_message = f"task result is None"
                return render(request, 'error_page.html', {'error_message': error_message})
        else:
            error_message = f"task is failed"
            return render(request, 'error_page.html', {'error_message': error_message})
    else:
        error_message = f"task is not ready"
        return render(request, 'error_page.html', {'error_message': error_message})
