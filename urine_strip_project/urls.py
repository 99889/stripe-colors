from django.urls import path
from urine_strip_app.views import process_image
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from urine_strip_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('process_image/', views.process_image, name='process_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)