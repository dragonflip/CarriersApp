"""
Definition of views.
"""

import random
import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import CreateUserForm
from .decorators import *

def index(request):
    return render(request, 'app/index.html')

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('main')
        else:
            #messages.info(request, 'Неправильне ім\'я або пароль.')
            context = {}
            return render(request, 'app/login.html', context)
    context = {}
    return render(request, 'app/login.html', context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password = form.cleaned_data['password2']
            user = authenticate(request, username=username, password=password)

            return redirect('login')

    context = {'form' : form}
    return render(request, 'app/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
