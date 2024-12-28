from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models



class CustomUser(AbstractUser):
    ROLES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=15, choices=ROLES, default='admin')
    
    def __str__(self):
        return self.username
    @property
    def created_courses(self):
        return self.course_set.all()
    
    @property
    def get_context_data(self):
        """Возвращает данные в зависимости от роли пользователя."""
        context = {
            'username': self.username,
            'email': self.email,
            'role': self.get_role_display(),
        }

        if self.role == 'student':
            context['courses'] = self.enrolled_courses.all()
        elif self.role == 'teacher':
            context['courses'] = self.created_courses.all()
        elif self.role == 'admin':
            from courses.models import Course  # Ленивая загрузка
            context['users_count'] = CustomUser.objects.count()
            context['courses_count'] = Course.objects.count()

        return context
    

    enrolled_courses = models.ManyToManyField(
        'courses.Course',
        blank=True,
        related_name='enrolled_users',
        help_text='Курсы, на которые записан студент',
    )

    # Связь One-to-Many для преподавателей
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
