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
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreateUserForm
from .decorators import *
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.views import View


def index(request):
    return render(request, 'app/index.html')

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)       

        if user is not None:
            if user.is_active:
               auth_login(request, user)
               return redirect('main')
            
            else:
                messages.error(
                request, 'Account is not active,please check your email')
            return render(request, 'login.html')

            auth_login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Неправильне ім\'я або пароль.')
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
            email = form.cleaned_data.get('email')
            email_qs = User.objects.filter(email=email)
            if not email_qs.exists():
                user = form.save()

                #first_name = form.cleaned_data['first_name']
                #last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                #password = form.cleaned_data['password2']

                #user = authenticate(request, username=email, password=password)
                user.set_password(password)
                user.save()

                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email_body = 'Привіт, ' + user.first_name + '! Для підтвердження реєстрації перейдіть за посиланням: \n' + activate_url

                email_subject = 'Успішна реєстрація'

                email_mes = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                    )

                email_mes.send(fail_silently=False)
                messages.success(request, 'На вашу пошту був надісланий лист з посиланням для підтвердження реєстрації.')
                return redirect('login')
            else:
                messages.info(request, 'Введена електронна пошта прив\'язана до іншого акаунта.')

    context = {'form' : form}
    return render(request, 'app/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'Account already activated.')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Акаунт був успішно активований.')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')



