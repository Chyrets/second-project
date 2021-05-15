from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from authy.models import Follow
from notification.models import Notification
from post.models import Likes, Comment


class LikeNotify:
    """
    Show like notification or delete it if follow remove like from some post
    """

    @staticmethod
    @receiver(post_save, sender=Likes)
    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.save()

    @staticmethod
    @receiver(post_delete, sender=Likes)
    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()


class CommentNotify:
    """
    Show comment notification or delete it if user delete his comment
    """

    @staticmethod
    @receiver(post_save, sender=Comment)
    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user

        notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_type=2)
        notify.save()

    @staticmethod
    @receiver(post_delete, sender=Comment)
    def user_delete_comment(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user

        notify = Notification.objects.filter(post=post, sender=sender, user=post.user, notification_type=2)
        notify.delete()


class FollowNotify:
    """
    Show follow notification or delete if sender unfollow user
    """

    @staticmethod
    @receiver(post_save, sender=Follow)
    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notification(sender=sender, user=following, notification_type=3)
        notify.save()

    @staticmethod
    @receiver(post_delete, sender=Follow)
    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notification.objects.filter(sender=sender, user=following, notification_type=3)
        notify.delete()
