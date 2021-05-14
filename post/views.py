from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from post.forms import AddPostForm, AddCommentForm
from post.models import Post, Stream, Likes, Tag, Comment
from post.permissions import AuthorPermissionMixin


class Wall(LoginRequiredMixin, View):
    """
    Wall if user posts
    """
    template_name = 'post/wall.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        posts = Stream.objects.filter(user=user)
        user_posts = Post.objects.filter(user=user)

        group_ids = []

        for post in posts:
            group_ids.append(post.post_id)

        for post in user_posts:
            group_ids.append(post.id)

        post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

        context = {
            'posts': post_items,
        }

        return render(request, self.template_name, context)


class PostDetailView(LoginRequiredMixin, View):
    """
    Display some post and info about him
    """
    form_class = AddCommentForm
    template_name = 'post/post_detail.html'

    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.form_class
        comments = Comment.objects.filter(post=post).order_by('date')

        context = {
            'post': post,
            'comments': comments,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[post_id]))

        return render(request, self.template_name, {'form': form})


class PostDeleteView(AuthorPermissionMixin, DeleteView):
    """
    Delete post
    """
    model = Post
    success_url = reverse_lazy('wall')

    def get_object(self, queryset=None):
        return Post.objects.get(id=self.kwargs.get("post_id"))


class AddPostVew(LoginRequiredMixin, View):
    """
    Display the form for add post
    """
    form_class = AddPostForm
    template_name = 'post/add_post.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = request.user
        tags_objs = []

        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split())

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user.id)
            p.tags.set(tags_objs)
            p.save()

            return redirect('wall')

        return render(request, self.template_name, {'form': form})


class LikeView(LoginRequiredMixin, View):
    """
    Display the form for add/remove like
    """
    def get(self, request, post_id):
        user = request.user
        post = Post.objects.get(id=post_id)
        current_likes = post.likes
        liked = Likes.objects.filter(user=user, post=post).count()

        if not liked:
            like = Likes.objects.create(user=user, post=post)
            current_likes += 1
        else:
            Likes.objects.filter(user=user, post=post).delete()
            current_likes -= 1

        post.likes = current_likes
        post.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TagView(LoginRequiredMixin, View):
    """
    Display post with some tag
    """

    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags=tag).order_by('-posted')

        context = {
            'posts': posts,
            'tag': tag
        }

        return render(request, 'post/tag.html', context)
