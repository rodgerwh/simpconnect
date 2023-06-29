from pathlib import Path
from PIL import Image

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ("UNKNOWN", "Not specified"),
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="UNKNOWN")
    profile_picture = models.ImageField(
        default="profile_pics/default_userpic.png", upload_to="profile_pics/"
    )
    liked_users = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="liked_by"
    )

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

        if (
            self.profile_picture
            and Path(self.profile_picture.name).name != "default_userpic.png"
        ):
            watermark_path = "media/watermark.png"
            image = Image.open(self.profile_picture.path)
            watermark = Image.open(watermark_path)

            width, height = image.size
            watermark_pos = (
                (width - watermark.width) // 2,
                (height - watermark.height) // 2,
            )

            image.paste(watermark, watermark_pos, mask=watermark)
            image.save(self.profile_picture.path)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
