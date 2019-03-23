from django.urls import path
from users.views import user_register_view, user_profile_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', user_register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('profile/', user_profile_view, name='profile'),
]
