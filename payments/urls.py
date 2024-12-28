from django.urls import path
from .views import *

app_name = 'payments'


urlpatterns = [
    path('success/<int:course_id>/', success, name='success'),
]

