from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='authy/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
    path('<username>/', views.UserProfileView.as_view(), name='profile'),
    path('<username>/follow/<option>', views.follow, name='follow'),
]
