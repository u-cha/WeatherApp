from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", LoginView.as_view(template_name="WeatherApp/login.html", next_page="index"), name="login"),
    path("register/", views.signup, name="register"),
]
