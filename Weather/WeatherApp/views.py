from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
import requests
from decouple import config
from . import models, forms
from django.forms import HiddenInput
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, template_name="WeatherApp/index.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, template_name="WeatherApp/register.html", context={"form": form})


def location_lookup(request):
    location_name = request.GET.get('name')
    response = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={location_name}&limit=5&appid={config("OPEN_WEATHER_API_KEY")}')
    result = {'location_name': location_name,
              'is_authenticated': request.user.is_authenticated,
              'username': request.user.username,
              'locations': response.json(),
              }
    return render(request, template_name="WeatherApp/lookup_results.html", context={"result": result})


def profile(request):
    if request.method == "POST":
        form = forms.LocationHiddenForm(request.POST)
        user = request.user
        location = models.Location(
                name=form.data["name"],
                latitude=form.data["latitude"],
                longitude=form.data["longitude"],
                country=form.data["country"])
        location.save()
        user.locations.add(location)
    user = request.user
    locations = User.objects.get(pk=user.pk).locations.all()
    return render(request, template_name="WeatherApp/profile.html", context={"locations": locations})


def log_out(request):
    logout(request)
    return redirect("index")
