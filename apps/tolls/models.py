from django.db import models

class TollRate(models.Model):
    VEHICLE_CHOICES = (
        ('car', 'Car'),
        ('threewheel', 'Threewheel'),
        ('bus', 'Bus'),
        ('truck', 'Truck'),
        ('motorbike', 'Motorbike'),
        ('van', 'Van'),
    )
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.get_vehicle_type_display()}: {self.rate}"
