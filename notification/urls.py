from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShowNotify.as_view(), name='show_notify'),
    path('<notify_id>/delete', views.DeleteNotify.as_view(), name='delete_notify')
]
