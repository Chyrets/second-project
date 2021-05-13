import uuid

from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    return f'user_{instance.user.username}/{filename}'


class Post(models.Model):
    """
    Post characteristics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, null=False)
    caption = models.TextField(max_length=1500)
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ImageField(default=0)

    def __str__(self):
        return str(self.id)
