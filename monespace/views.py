from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Event, Location, User
from .forms import UserCreationForm, UserAuthenticationForm, EventForm, LocationForm


def index(request):
    all_events = Event.objects.all()
    all_locations = Location.objects.all()
    return render(request, 'index.html', context={"events":all_events, 'locations':all_locations})


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

    return render(request, 'login.html', context={"form":form})


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            new_user.save()
            login(request, new_user)
            return redirect('index')
    return render(request, 'register.html', context={"form":form})


@login_required(login_url='/login/')
def event_create(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'event.html', context={"form":form})


@login_required(login_url='/login/')
def event_edit(request, event_id):
    event_page = Event.objects.get(id=event_id)
    form = EventForm(instance=event_page)
    if request.method == "POST":
        form = EventForm(data=request.POST)
        if form.is_valid():
            event_page.name = form.cleaned_data['name']
            event_page.description = form.cleaned_data['description']
            event_page.date = form.cleaned_data['date']
            event_page.time_from = form.cleaned_data['time_from']
            event_page.time_to = form.cleaned_data['time_to']
            try:
                event_page.location = Location.objects.get(id=request.POST['location'])
            except:
                event_page.location = None
            event_page.save()
            return redirect('index')
    return render(request, 'event.html', context={"form":form, 'is_edit':True, 'event_id':event_id})


@login_required(login_url='/login/')
def event_details(request, event_id):
    event_page = Event.objects.get(id=event_id)
    if event_page:
        return render(request, 'event_details.html', context={"event": event_page})
    return redirect('index')


@login_required(login_url='/login/')
def location_create(request):
    form = LocationForm()
    if request.method == "POST":
        form = LocationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'location.html', context={"form":form})


@login_required(login_url='/login/')
def location_edit(request, location_id):
    location_page = Location.objects.get(id=location_id)
    form = LocationForm(instance=location_page)
    if request.method == "POST":
        form = LocationForm(data=request.POST)
        if form.is_valid():
            location_page.name = form.cleaned_data['name']
            location_page.address_number = form.cleaned_data['address_number']
            location_page.address = form.cleaned_data['address']
            location_page.address_2 = form.cleaned_data['address_2']
            location_page.city = form.cleaned_data['city']
            location_page.zip_code = form.cleaned_data['zip_code']
            location_page.country = form.cleaned_data['country']
            try:
                location_page.manager_location = User.objects.get(id=request.POST['manager_location'])
            except:
                location_page.manager_location = None
            location_page.save()
            return redirect('index')
    return render(request, 'location.html', context={"form":form, 'is_edit':True, 'location_id':location_id})


@login_required(login_url='/login/')
def location_details(request, location_id):
    location_page = Location.objects.get(id=location_id)
    if location_page:
        return render(request, 'location_details.html', context={"location": location_page})
    return redirect('index')


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('index')
