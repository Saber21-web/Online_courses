from django.contrib import admin
from django.urls import path, include
from app import settings
from courses.views import course_list
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('payments/', include('payments.urls')),
    path('', course_list, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
