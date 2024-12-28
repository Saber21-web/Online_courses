from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Category)
@admin.register(CoursePart)
class CoursePartAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'is_free')

@admin.register(CoursePurchase)
class CoursePurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'purchase_date')
    
admin.site.register(Comment)