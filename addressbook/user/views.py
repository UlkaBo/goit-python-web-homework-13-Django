from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import transaction


from user.api import create_user
from ab.api import create_new_abonent

# Create your views here.


def _validate_data(username, password):
    error = None
    if not username:
        raise BadRequestException('Username in required')
    if not password:
        raise BadRequestException('Password is required')

    return error


def register_view(request):
    x = request.user
    print('----------', x.username)
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'user/register.html')
    username = request.POST['username']
    email = request.POST['email'] or ''
    password = request.POST['password']
    try:
        _validate_data(username, password)
    except BadRequestException as e:
        messages.add_message(request, messages.ERROR, e.msg)
        return render(request, 'user/register.html')

    user_exists = User.objects.filter(username=username).exists()
    if user_exists:
        messages.add_message(request, messages.ERROR,
                             'Username already exists')
        return render(request, 'user/register.html')

    with transaction.atomic():
        user = create_user(username, email, password)

    return redirect(reverse('auth:login'))


def login_view(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    username = request.POST['username']
    #email = request.POST['email']
    password = request.POST['password']
    try:
        _validate_data(username, password)
    except BadRequestException as e:
        messages.add_message(request, messages.ERROR, e.msg)
        return render(request, 'user/login.html')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect(reverse('ab:index'))
    else:
        messages.add_message(request, messages.ERROR,
                             'Username or password is incorrect')
        return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'user/login.html')
