from django.urls import path
from django.contrib.auth.views import LoginView
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="WeatherApp/login.html", next_page="index"), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("location/search/", views.location_search, name='location_lookup'),
    path("location/delete/", views.location_delete, name="location_delete"),
    path("location/add/", views.location_add, name="location_add"),
    path("weather/show/", views.weather_show, name="weather_show"),
]
