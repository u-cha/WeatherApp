from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Location(models.Model):
    name = models.CharField()
    users = models.ManyToManyField(User, related_name='locations')
    latitude = models.DecimalField(max_digits=7, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    country = models.CharField()

    class Meta:
        unique_together = ('latitude', 'longitude',)

    def __str__(self):
        return f"{self.name}: lat={self.latitude}, lon={self.longitude}"
