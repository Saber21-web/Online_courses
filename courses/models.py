from django.db import models
from app import settings
from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.name
    

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    purchased_by = models.ManyToManyField(CustomUser, through='CoursePurchase', related_name='purchased_courses')
    payment_link = models.URLField(null=True, blank=True)
    has_purchased = models.BooleanField(default=False)
    
    stripe_product_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
class CoursePart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="parts")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    is_free = models.BooleanField(default=False)
    video = models.FileField(upload_to='course_parts/', blank=True, null=True)
    
class CoursePurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.user} -> {self.course} - {self.text[:7]}...'
