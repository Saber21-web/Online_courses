from django.http import  JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from courses.models import Course
from users.models import CustomUser
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return redirect('courses:course_list') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print(f"Попытка логина: username={username}, password={password}")  # Отладка

            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Пользователь успешно аутентифицирован!")  # Отладка
                login(request, user)
                return redirect('courses:course_list')
            else:
                print("Неверный username или пароль.")  # Отладка
                form.add_error(None, "Неверный username или пароль")
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    
    # Проверяем, был ли запрос отправлен через AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Если запрос был AJAX, возвращаем JSON-ответ
        return JsonResponse({'success': True})
    
    # Если обычный запрос, перенаправляем на страницу курса
    return redirect('courses:course_list')

@login_required
def profile(request, id):
    # Получаем пользователя по ID
    user = get_object_or_404(CustomUser, id=id)
    
    # Используем метод get_context_data выбранного пользователя
    context = user.get_context_data

    return render(request, 'users/profile.html', context)

