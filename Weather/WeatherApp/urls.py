from django.urls import path
from django.contrib.auth.views import LoginView
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", LoginView.as_view(template_name="WeatherApp/login.html", next_page="index"), name="login"),
    path("register/", views.register, name="register"),
    path("lookup/<str:location_name>", views.location_lookup, name='location_lookup'),
    path("profile/", views.profile, name="profile"),
]
