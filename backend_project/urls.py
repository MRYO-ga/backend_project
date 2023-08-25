#url.py
from django.urls import path
from django.views.generic import RedirectView
from backend_app import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='upload_image'), name='default_redirect'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
