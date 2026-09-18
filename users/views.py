from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import RegisterForm

# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return redirect('products:list')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать в Hop & Barley')
            return redirect('products:list')

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:list')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        print('EMAIL:', email)
        print('USER:', user)

        if user is not None:
            login(request, user)
            messages.success(request, 'Добро пожаловать')
            return redirect('products:list')

        messages.error(request, 'Неверный email или пароль')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('products:list')
