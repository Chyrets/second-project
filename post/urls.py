from django.urls import path

from . import views

urlpatterns = [
    path('', views.Wall.as_view(), name='wall'),
    path('<uuid:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('new-post', views.AddPostVew.as_view(), name='new_post'),
    path('<uuid:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<uuid:post_id>/likes/', views.LikeView.as_view(), name='post_like'),
    path('tag/<slug:tag_slug>/', views.TagView.as_view(), name='tags'),
]
