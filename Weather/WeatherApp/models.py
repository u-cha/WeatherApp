from django.db import models
from django.contrib.auth.models import User
import json


class Weather:
    def __init__(self, short_type: str, temperature: float, description: str):
        self.short_type = short_type
        self.temperature = temperature
        self.description = description

    @staticmethod
    def from_json(weather_json):
        weather_dict = weather_json
        try:
            short_type = weather_dict["weather"][0]["main"]
            temperature = weather_dict["main"]["temp"]
            description = weather_dict["weather"][0]["description"]
        except KeyError:
            return False
        return Weather(short_type=short_type, temperature=temperature, description=description)


class Location(models.Model):
    name = models.CharField()
    users = models.ManyToManyField(User, related_name='locations')
    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    country = models.CharField()

    class Meta:
        unique_together = ('latitude', 'longitude',)

    def __str__(self):
        return f"{self.name}: lat={self.latitude}, lon={self.longitude}"
