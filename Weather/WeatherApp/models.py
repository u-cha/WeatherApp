from django.db import models
from django.contrib.auth.models import User


class Weather:
    def __init__(self, short_type: str, temperature: float, description: str):
        self.short_type = short_type
        self.temperature = temperature
        self.description = description


class Location(models.Model):
    name = models.CharField()
    users = models.ManyToManyField(User, related_name='locations')
    latitude = models.DecimalField(max_digits=23, decimal_places=20)
    longitude = models.DecimalField(max_digits=23, decimal_places=20)
    country = models.CharField()

    class Meta:
        unique_together = ('latitude', 'longitude',)

    def __str__(self):
        return f"{self.name}: lat={self.latitude}, lon={self.longitude}"
