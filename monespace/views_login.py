from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import UserCreateForm, UserAuthenticationForm


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
            new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                password=form.cleaned_data['password1'])
            new_user.save()
            login(request, new_user)
            return redirect('index')
    return render(request, 'register.html', context={"form": form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('index')