from django.conf import settings
from django.db import models


class Route(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    airline = models.CharField(max_length=2)
    baseline_price = models.FloatField()
    threshold = models.FloatField(default=0.5)

    def __str__(self):
        return f"{self.origin}-{self.destination} {self.airline}"


class PriceHistory(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.route}: {self.price} at {self.timestamp}"
