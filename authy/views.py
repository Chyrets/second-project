from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from authy.forms import SignupForm, EditProfileForm, ChangePasswordForm
from authy.models import Profile, Follow
from post.models import Stream, Post


class UserProfileView(View):
    """
    Display user profile
    """

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
        posts = Post.objects.filter(user=user).order_by('-posted')

        post_count = Post.objects.filter(user=user).count()
        following_count = Follow.objects.filter(follower=user).count()
        followers_count = Follow.objects.filter(following=user).count

        context = {
            'profile': profile,
            'posts': posts,
            'follow_status': follow_status,
            'post_count': post_count,
            'following_count': following_count,
            'followers_count': followers_count,
        }

        return render(request, 'authy/profile.html', context)


class SignupView(View):
    """
    Display user signup form
    """
    form_class = SignupForm
    template_name = 'authy/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')

        return render(request, self.template_name, {'form': form})


class EditProfileView(LoginRequiredMixin, View):
    """
    Display the form for editing user profile
    """
    form_class = EditProfileForm
    template_name = 'authy/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        profile = Profile.objects.get(user_id=request.user.id)
        return render(request, self.template_name, {'form': form, 'profile': profile})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        profile = Profile.objects.get(user_id=request.user.id)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('profile', username=request.user.username)

        return render(request, self.template_name, {'form': form})


class PasswordChangeView(LoginRequiredMixin, View):
    """
    Display the form for changing user password
    """
    form_class = ChangePasswordForm
    template_name = 'authy/change_password.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('profile', username=request.user.username)

        return render(request, self.template_name, {'form': form})


@login_required
def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following)

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.posted, following=following)
                    stream.save()

        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))
