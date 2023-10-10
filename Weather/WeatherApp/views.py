from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import requests
from decouple import config


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


def location_lookup(request, location_name):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location_name}&appid={config("OPEN_WEATHER_API_KEY")}&units=metric')
    result = response.json()
    return render(request, template_name="WeatherApp/lookup_results.html", context={"result": result})
