from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View

from direct.models import Message


class DirectView(LoginRequiredMixin, View):
    """
    Display direct list of messages
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        messages = Message.get_messages(user=user)
        active_direct = None
        directs = None

        if messages:
            message = messages[0]
            active_direct = message['user'].username
            directs = Message.objects.filter(user=user, recipient=message['user'])
            directs.update(is_read=True)

            for message in messages:
                if message['user'].username == active_direct:
                    message['unread'] = 0

        context = {
            # 'directs': directs,
            'messages': messages,
            'active_direct': active_direct
        }

        return render(request, 'direct/direct.html', context)


class DirectMessageView(LoginRequiredMixin, View):
    """
    Display message from some user
    """

    def get(self, request, username, *args, **kwargs):
        user = request.user
        messages = Message.get_messages(user=user)
        active_direct = username
        directs = Message.objects.filter(user=user, recipient__username=username)
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == username:
                message['unread'] = 0

        context = {
            'directs': directs,
            'messages': messages,
            'active_direct': active_direct
        }

        return render(request, 'direct/direct.html', context)


class SendMessageView(LoginRequiredMixin, View):
    """
    Display form for send message
    """

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        from_user = request.user
        username = request.POST.get('to_user')
        body = request.POST.get('body')

        to_user = User.objects.get(username=username)
        Message.send_message(from_user, to_user, body)

        return redirect('direct')


class SearchUserView(LoginRequiredMixin, View):
    """
    Display form for search user
    """

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        context = {}

        if query:
            users = User.objects.filter(Q(username__icontains=query))

            paginator = Paginator(users, 6)
            page_number = request.GET.get('page')
            users_paginator = paginator.get_page(page_number)

            context = {
                'users': users_paginator,
            }

        return render(request, 'direct/search_user.html', context)


class NewChatView(LoginRequiredMixin, View):
    """
    Display form for start new chat
    """

    def get(self, request, username, *args, **kwargs):
        from_user = request.user
        body = 'hello!'

        try:
            to_user = User.objects.get(username=username)
        except Exception:
            return redirect('user_search')

        if from_user != to_user:
            Message.send_message(from_user, to_user, body)

        return redirect('direct')
