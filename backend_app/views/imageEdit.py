from django.shortcuts import render
from ..forms import UploadImageForm, EditImageForm 
from ..models import UserImage, Image, Tag
from ..tasks import process_and_save_image
import traceback
from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import User
import base64
from urllib.parse import unquote

DEBUG = False


# 原方案
def imageEdit(request):
    if request.method == "POST":
        form = EditImageForm(request.POST, request.FILES)
        if form.is_valid():
            print("start upload_image...")
            user_id = form.cleaned_data["user_id"]
            image = form.clean_image()

            try:
                user_image = UserImage(
                    user_id=user_id,
                    src_face_index=input_face_index,
                    dst_face_index=output_face_index,
                    first_image=first_image,
                    second_image=second_image,
                )
                user_image.save()

                # 将图像处理任务添加到Celery队列中，不等待任务完成
                task = process_and_save_image.apply_async(args=[user_image.id])
                user_image.task_id = task.id
                user_image.status = "PENDING"
                user_image.save()
                print("start process_and_save_image...")

                # 立即返回响应，告知前端任务已启动
                response_data = {
                    "status": "PENDING",
                    "task_id": task.id,
                    "user_id": user_id,
                }
                if DEBUG:
                    return redirect("check_task_status", task_id=task.id)
                else:
                    return JsonResponse(response_data)
            except Exception as e:
                error_message = (
                    f"upload_image: An error occurred while processing the image: {e}"
                )
                traceback.print_exc()
                return JsonResponse(
                    {"status": "FAILURE", "error_message": error_message}, status=500
                )
        else:
            print(form.errors)
            return JsonResponse(
                {"status": "FAILURE", "error_message": form.errors}, status=400
            )
    else:
        form = UploadImageForm()
        return render(request, "upload_image.html", {"form": form})


