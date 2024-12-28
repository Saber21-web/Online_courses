from django.db import models
from users.models import CustomUser 
from courses.models import Course

class Payment(models.Model):
    user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('pending', 'Pending'), ('failed', 'Failed')])

    def __str__(self):
        return f"{self.user.email} - {self.course.title} - {self.amount}$"
    