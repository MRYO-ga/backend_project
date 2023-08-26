#models.py
from django.db import models
from PIL import Image
from PIL import Image
from io import BytesIO
import tempfile
from .image_utils import process_image

class UserImage(models.Model):
    user_id = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_images/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

    def save(self, *args, **kwargs):
        if not self.processed_image:
            processed_image = process_image(self.image)
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_image:
                processed_image.save(temp_image, format='JPEG')
                self.processed_image.save(self.image.name, temp_image, save=False)
                print("Processed image saved to processed_image field.")
        super().save(*args, **kwargs)
        print("Processed image saved sucessed")

    class Meta:
        app_label = 'backend_app'
