import uuid

from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

from authy.models import Follow


def user_directory_path(instance, filename):
    return f'user_{instance.user.username}/{filename}'


class Tag(models.Model):
    """
    Tag for post
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    """
    Post characteristics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, null=False)
    caption = models.TextField(max_length=1500)
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        SIZE = 600, 600

        if self.picture:
            picture = Image.open(self.picture.path)
            picture.thumbnail(SIZE, Image.LANCZOS)
            picture.save(self.picture.path)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return str(self.id)


class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    @staticmethod
    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')


class Comment(models.Model):
    """
    Comments for post
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)


post_save.connect(Stream.add_post, sender=Post)
