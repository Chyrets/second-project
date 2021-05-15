from django.shortcuts import render, redirect
from django.views import View

from notification.models import Notification


class ShowNotify(View):
    """
    Display notification
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        notification = Notification.objects.filter(user=user).order_by('-date')
        Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

        return render(request, 'notification/notification.html', {'notify': notification})


class DeleteNotify(View):
    """
    Delete notification
    """

    def get(self, request, notify_id):
        Notification.objects.filter(id=notify_id, user=request.user).delete()
        return redirect('show_notify')


def count_notification(request):
    count_notify = 0
    if request.user.is_authenticated:
        count_notify = Notification.objects.filter(user=request.user, is_seen=False).count()

    return {'count_notify': count_notify}