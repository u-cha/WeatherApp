from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
import requests
from decouple import config
from . import models, forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.db.models import Q

from .services.weatherapiservice import WeatherAPIService


def index(request):
    return render(request, template_name="WeatherApp/index.html")


def register(request):
    if request.method != "POST":
        form = UserCreationForm()
        return render(request, template_name="WeatherApp/register.html", context={"form": form})
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')


def location_search(request):
    search_query = request.GET.get("name")
    response = WeatherAPIService.get_locations_by_name(search_query)
    search_result = {"search_query": search_query,
                     "locations": response.payload,
                     "error": response.error_message,
                     }
    return render(request, template_name="WeatherApp/lookup_results.html", context={"search_result": search_result})


@login_required(login_url="login")
def profile(request):
    user = request.user
    locations = User.objects.get(pk=user.pk).locations.all()
    locations_with_weather = [{"location": location,
                               "weather": WeatherAPIService.get_weather_by_location(location).payload
                               }
                              for location in locations]
    return render(request, template_name="WeatherApp/profile.html",
                  context={"locations_with_weather": locations_with_weather})


@login_required(login_url="index")
def log_out(request):
    logout(request)
    return redirect("index")


@login_required(login_url="index")
def location_delete(request):
    if request.method == "POST":
        form = forms.LocationHiddenForm(request.POST)
        latitude = form.data["latitude"]
        longitude = form.data["longitude"]
        user = request.user
        location = models.Location.objects.get(latitude=latitude, longitude=longitude)
        user.locations.remove(location)
        return redirect("profile")


def weather_lookup(request):
    if request.method == "GET":
        form = forms.LocationHiddenForm(request.GET)
        location = models.Location(
            name=form.data["name"],
            latitude=form.data["latitude"],
            longitude=form.data["longitude"],
            country=form.data["country"])
        weather = WeatherAPIService.get_weather_by_location(location).payload
        return render(request, "WeatherApp/weather_show.html", context={"location": location, "weather": weather})


@login_required(login_url="index")
def location_add(request):
    if request.method == "POST":
        form = forms.LocationHiddenForm(request.POST)
        user = request.user
        location = models.Location(
            name=form.data["name"],
            latitude=form.data["latitude"],
            longitude=form.data["longitude"],
            country=form.data["country"])
        try:
            location.save()
        except IntegrityError:
            location = models.Location.objects.get(latitude=form.data["latitude"], longitude=form.data["longitude"])
        try:
            user.locations.add(location)
        except IntegrityError:
            pass
    return redirect("profile")

