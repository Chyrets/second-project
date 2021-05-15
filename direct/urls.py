from django.urls import path

from . import views

urlpatterns = [
    path('', views.DirectView.as_view(), name='direct'),
    path('<username>/', views.DirectMessageView.as_view(), name='direct_message'),
    path('send', views.SendMessageView.as_view(), name='send_message'),
    path('search', views.SearchUserView.as_view(), name='user_search')
]
