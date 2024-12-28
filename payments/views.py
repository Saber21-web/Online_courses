from django.shortcuts import redirect, render
from courses.models import Course
import stripe
from app import settings
from .forms import PaymentForm
from django.contrib import messages
from django.shortcuts import get_object_or_404


stripe.api_key = settings.STRIPE_SECRET_KEY



def success(request, course_id):
    # Получение курса
    course = get_object_or_404(Course, id=course_id)
    
    # Проверка: купил ли пользователь курс
    has_purchased = course.purchased_by.filter(id=request.user.id).exists()

    if request.method == 'POST':
        # Проверка успешной оплаты (например, передается через POST)
        if request.POST.get('success') == 'true' and not has_purchased:
            # Добавление пользователя в список покупателей
            course.purchased_by.add(request.user)
            course.save()
            print(f"Пользователь {request.user} добавлен в список покупателей.")
            
            # Уведомление об успешной покупке
            messages.success(request, "Вы успешно приобрели курс и получили доступ к материалам!")
            return redirect('courses:course_detail', pk=course.id)
        else:
            messages.error(request, "Произошла ошибка при обработке покупки.")
            return redirect('courses:course_list')

    # Если метод GET, показать страницу успеха
    return render(request, 'payments/success.html', {'course': course, 'has_purchased': has_purchased})
