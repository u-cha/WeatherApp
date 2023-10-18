from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone


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


class Weather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="weather")
    short_type = models.CharField()
    temperature = models.FloatField()
    description = models.CharField()
    obtained_at = models.DateTimeField(auto_now_add=git True)

    class Meta:
        get_latest_by = "obtained_at"

    def __str__(self):
        return f"Weather in {self.location} obtained at {self.obtained_at}"
