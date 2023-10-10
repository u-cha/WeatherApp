from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return HttpResponse("Hello from WeatherApp")


def register(request):
    if request.method == "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, template_name="WeatherApp/register.html", context={"form": form})
