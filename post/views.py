from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from post.models import Post


class Wall(LoginRequiredMixin, View):
    """
    Wall if user posts
    """
    template_name = 'post/wall.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(user=user)

        context = {
            'posts': posts,
        }

        return render(request, self.template_name, context)
