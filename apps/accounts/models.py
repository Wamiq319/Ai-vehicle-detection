from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('operator', 'Operator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    plain_password = models.CharField(max_length=128, blank=True, null=True, help_text="Store original password for operator onboarding (optional)")

    def __str__(self):
        return f"{self.username} ({self.role})"


class OperatorProfile(models.Model):
    """
    Additional details for operators (toll booth staff or camera operators)
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='operator_profile')
    assigned_toll_point = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Operator: {self.user.username} - {self.assigned_toll_point}"
