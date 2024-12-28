from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [
    path('course_list/', course_list, name='course_list'),
    path('course_detail/<int:pk>/', course_detail, name='course_detail'),
    path('create/', course_create, name='course_create'),
    path('course_update/<int:pk>/', course_update, name='course_update'),
    path('course_delete/<int:pk>/', course_delete, name='course_delete'),
    path('part/<int:course_id>/', course_part, name='course_part'),
    path('edit_part/<int:part_id>/', edit_course_part, name='edit_course_part'),
    path('delete_part/<int:part_id>/', delete_course_part, name='delete_course_part'),
    path('comment_delete/<int:coment_id>/', comment_delete, name='comment_delete'),
]
