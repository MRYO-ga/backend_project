# views.py
from django.shortcuts import render
from .models import UserImage

def upload_image(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        image = request.FILES['image']

        user_image = UserImage(user_id=user_id, image=image)
        user_image.save()

        uploaded_image_url = user_image.image.url
        processed_image_url = user_image.processed_image.url
        return render(request, 'image_display.html', {'uploaded_image_url': uploaded_image_url, 'processed_image_url': processed_image_url})
    
    return render(request, 'upload_image.html')