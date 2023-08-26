# backend_app/views.py
from django.shortcuts import render
from .forms import UploadImageForm
from .models import UserImage
from django.core.exceptions import ValidationError
import traceback

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            image = form.cleaned_data['image']

            try:
                user_image = UserImage(user_id=user_id, image=image)
                user_image.save()
                return render(request, 'image_display.html', {'uploaded_image_url': user_image.image.url, 'processed_image_url': user_image.processed_image.url})
            except Exception as e:
                error_message = f"An error occurred while processing the image: {e}"
                traceback.print_exc()
        else:
            error_message = "Invalid form submission. Please check the data."

        return render(request, 'upload_image.html', {'form': form, 'error_message': error_message})
    else:
        form = UploadImageForm()
        return render(request, 'upload_image.html', {'form': form})
