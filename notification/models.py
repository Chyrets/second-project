from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    """
    Notification for like, comment, follow
    """
    NOTIFICATION_TYPES = (
        (1, 'Like'),
        (2, 'Comment'),
        (3, 'Follow')
    )

    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='notify_post', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_from_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
