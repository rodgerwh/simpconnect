from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ("UNKNOWN", "Not specified"),
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="UNKNOWN")
    profile_picture = models.ImageField(
        default="profile_pics/default_userpic.png", upload_to="profile_pics/"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
