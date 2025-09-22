# detections/models.py
from django.db import models
from django.utils import timezone
from apps.tolls.models import TollRate

class Detection(models.Model):
    VEHICLE_CHOICES = (
        ('truck', 'Truck'),
        ('car', 'Car'),
        ('bolan', 'Bolan'),
    )

    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES)
    toll_rate = models.DecimalField(max_digits=10, decimal_places=2)
    detected_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.vehicle_type} - {self.toll_rate} RS @ {self.detected_at.strftime('%Y-%m-%d %H:%M:%S')}"
