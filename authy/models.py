import os

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    picture_name = f'user_{instance.user.id}/profile.jpg'
    full_path = os.path.join(settings.MEDIA_ROOT, picture_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return picture_name


class Profile(models.Model):
    """
    Profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    profile_info = models.TextField(max_length=5000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        SIZE = 300, 300

        if self.picture:
            picture = Image.open(self.picture.path)
            picture.thumbnail(SIZE, Image.LANCZOS)
            picture.save(self.picture.path)

    def __str__(self):
        return self.user.username
