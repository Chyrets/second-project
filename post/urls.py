from django.urls import path

from post.views import Wall

urlpatterns = [
    path('', Wall.as_view(), name='wall'),
]
