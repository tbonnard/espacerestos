from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import string
import random


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


from .forms import UserCreateForm, UserAuthenticationForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserAuthenticationForm()
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            return redirect('index')

    return render(request, 'login.html', context={"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserCreateForm()
    if request.method == "POST":
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('select_locations')
    return render(request, 'register.html', context={"form": form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('index')


def generate_user_temp_password_key():
    uid_key_generated = [random.choice(string.ascii_letters + string.digits) for i in range(50)]
    uid_key = "".join(uid_key_generated)
    return uid_key


# def password_reset_email(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = PasswordResetForm(data=request.POST)
#             if form.is_valid():
#                 email = form.cleaned_data['email']
#                 for i in User.objects.all():
#                     if email == i.email:
#                         user_key = generate_user_temp_password_key()
#                         i.password_key = user_key
#                         i.save()
#                         print('email to send')
#             return redirect('reset_password_email_sent')
#         else:
#             form = PasswordResetForm()
#             return render(request, 'reset_password_email.html', context={"form": form})
#     return redirect('index')

#
# def reset_password_email_sent(request):
#     if not request.user.is_authenticated:
#         return render(request, 'reset_password_email_sent.html')
#     return redirect('index')
#
#
# def reset_password(request):
#     if not request.user.is_authenticated:
#         try:
#             user_key = request.GET.get('key')
#             user = User.objects.filter(password_key=user_key)
#         except:
#             return redirect('index')
#         else:
#
#             if request.method == "POST":
#                 form = SetPasswordForm(user=user, data=request.POST)
#                 if form.is_valid():
#                     user_updated_pwd = form.save()
#                     user_updated_pwd.password_key = ''
#                     user_updated_pwd.save()
#                     return render(request, 'reset_password_success.html')
#             else:
#                 form = SetPasswordForm(user=user)
#                 return render(request, 'reset_password.html', context={"form": form, "key":user_key})
#
#     return redirect('index')
#
#
# def reset_password_success(request):
#     if not request.user.is_authenticated:
#         return render(request, 'reset_password_success.html')
#     return redirect('index')
