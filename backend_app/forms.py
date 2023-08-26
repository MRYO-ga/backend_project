# backend_app/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UploadImageForm(forms.Form):
    user_id = forms.CharField(max_length=100)
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image.content_type.startswith('image'):
            raise ValidationError(_('File is not an image.'))
        return image
