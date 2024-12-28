from django import forms
from .models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'price', 'video', 'category', 'payment_link']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'instructor': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'video': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'payment_link': forms.URLInput(attrs={'class': 'form-control form-control-sm'}),
        }
class CoursePartForm(forms.ModelForm):
    class Meta:
        model = CoursePart
        fields = ['title', 'content', 'is_free', 'video']

