from django.conf import settings
import stripe
from .models import Course, Category
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


app_name = 'courses'
stripe.api_key = settings.STRIPE_SECRET_KEY

def course_list(request):
    # Получение параметров из GET-запроса
    category_id = request.GET.get('category')  # Фильтр по категории
    search_query = request.GET.get('search', '')  # Поисковый запрос
    sort_by = request.GET.get('sort')  # Сортировка

    # Начальный набор курсов
    courses = Course.objects.all()

    # Фильтр по категории
    if category_id:
        courses = courses.filter(category_id=category_id)

    # Поиск по названию
    if search_query:
        courses = courses.filter(title__icontains=search_query)

    # Сортировка курсов
    if sort_by == 'newest':
        courses = courses.order_by('-created_at')  # Сначала новые
    elif sort_by == 'price':
        courses = courses.order_by('price')  # По возрастанию це
    # Получение всех категорий для отображения в фильтрах
    categories = Category.objects.all()

    # Передача данных в шаблон
    return render(request, 'courses/course_list.html', {
        'courses': courses,  # Курсы
        'categories': categories,  # Категории для фильтрации
        'selected_category': category_id,  # Выбранная категория
        'search_query': search_query,  # Поисковый запрос
        'sort_by': sort_by,  # Текущая сортировка
    })


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)  # Не забудьте добавить request.FILES для загрузки файлов
        if form.is_valid():
            # Сохраняем курс в базе данных
            course = form.save(commit=False)  # Не сохраняем еще в БД
            course.instructor = request.user  # Устанавливаем текущего пользователя как инструктора
            course.save()  # Теперь сохраняем курс

            # Создание продукта в Stripe
            product = stripe.Product.create(
                name=course.title,
                description=course.description,
            )

            # Создание цены в Stripe
            price = stripe.Price.create(
                unit_amount=int(course.price * 100),  # Указываем цену в центах
                currency='usd',  # Укажите нужную валюту
                product=product.id,
            )

            # Сохраняем идентификаторы Stripe в модели Course
            course.stripe_product_id = product.id
            course.stripe_price_id = price.id
            course.save()  # Сохраняем изменения в модели Course

            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_create.html', {'form': form})


def course_detail(request, pk):
    # Получаем курс
    course = get_object_or_404(Course, pk=pk)

    # Проверка, приобрел ли пользователь курс
    has_purchased = course.purchased_by.filter(id=request.user.id).exists()
    print(has_purchased)
    if request.method == 'POST':

        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            Comment.objects.create(
                course=course,
                user=request.user,
                text=comment_text
            )
            return redirect('courses:course_detail', pk=course.id)
        # Проверка успешной оплаты и статуса покупки
        if request.POST.get('success') == 'true' and not has_purchased:
            # Добавление пользователя в список покупателей
            course.purchased_by.add(request.user)
            course.save()

            messages.success(request, "Вы успешно приобрели курс и получили доступ ко всем его материалам!")
        else:
            messages.warning(request, "Вы уже приобрели этот курс или произошла ошибка.")

    # Отображение страницы курса
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'has_purchased': has_purchased,
    })

@login_required
def course_update(request, pk):
    # Получение объекта Course по pk
    course = get_object_or_404(Course, id=pk)
    form = CourseForm(instance=course)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:course_detail', pk=course.id)

    context = {
        'form': form,
        'course': course,
    }

    return render(request, 'courses/course_update.html', context)

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # Разрешить удаление только владельцу курса или администратору
    if request.user == course.instructor or request.user.is_superuser:
        if request.method == 'POST':
            # Удаление курса
            course.delete()
            return redirect('courses:course_list')  # Перенаправление на список курсов
        return render(request, 'courses/course_delete.html', {'course': course})  # Отображение страницы подтверждения
    else:
        return redirect('courses:course_detail', pk=pk)  # Если нет прав на удаление, перенаправляем на детали курса

@login_required
def course_part(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CoursePartForm(request.POST, request.FILES)
        if form.is_valid():
            part = form.save(commit=False)
            part.course = course
            part.save()
            return redirect('courses:course_detail', pk=course.id)
    else:
        form = CoursePartForm()

    return render(request, 'courses/course_part.html', {'form': form, 'course': course})

@login_required
def edit_course_part(request, part_id):
    part = get_object_or_404(CoursePart, id=part_id)

    if request.method == "POST":
        form = CoursePartForm(request.POST, request.FILES, instance=part)
        if form.is_valid():
            form.save()
            return redirect('courses:course_detail', pk=part.course.id)
    else:
        form = CoursePartForm(instance=part)

    return render(request, 'courses/course_edit_part.html', {'form': form, 'part': part})

@login_required
def delete_course_part(request, part_id):
    # Получаем объект CoursePart или возвращаем 404, если не найден
    part = get_object_or_404(CoursePart, id=part_id)
    
    # Если запрос POST, то удаляем объект
    if request.method == "POST":
        # Сохраняем course_id до удаления
        course_id = part.course.id
        part.delete()  # Удаляем раздел курса
        
        # Перенаправляем на страницу с деталями курса
        return redirect('courses:course_detail', pk=course_id)
    
    # Если запрос GET, показываем страницу подтверждения удаления
    return render(request, 'courses/course_delete_part.html', {'part': part})

def comment_delete(request, coment_id):
    coment = get_object_or_404(Comment, pk=coment_id)
    course_id = coment.course.id
    coment.delete()
    return redirect('courses:course_detail', pk=course_id)
