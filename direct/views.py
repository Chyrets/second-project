from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View

from direct.models import Message


def get_messages(user):
    """
    Function for receiving messages
    :param user: the user for whom the messages is displayed
    :return: list of users with whom the user has a chat
    """
    users = []
    messages = Message.objects.filter(user=user).values('recipient').annotate(last=Max('date')).order_by('-last')
    for message in messages:
        users.append({
            'user': User.objects.get(pk=message['recipient']),
            'last': message['last'],
            'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()
        })
    return users


def send_message(from_user, to_user, body):
    """
    Function for sending messages
    :param from_user: from whom the user received the message
    :param to_user: who got the message
    :param body: message text
    :return: message to sender
    """
    sender_message = Message(
        user=from_user,
        sender=from_user,
        recipient=to_user,
        body=body,
        is_read=True
    )
    sender_message.save()

    recipient_message = Message(
        user=to_user,
        sender=from_user,
        body=body,
        recipient=from_user,
    )
    recipient_message.save()
    return sender_message


class DirectView(LoginRequiredMixin, View):
    """
    Display direct list of messages
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        messages = get_messages(user=user)
        active_direct = None

        context = {
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
        messages = get_messages(user=user)
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
        send_message(from_user, to_user, body)

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
