from django.urls import path
from users.views import user_register_view, user_profile_view
from django.contrib.auth import views as auth_views


urlpatterns = [

    # Register – Register page
    # Login – login page. Hyperlink for “forget password” and ”Sign up” are included.
    # Logout – Extend successful log out statement to “base.html”
    # Password reset – Forget password page. A password reset link will be sent to user email
    # Password reset done – Extend email successfully sent statement to “base.html”
    # Password reset confirmation – Reset pass word page.
    # Password reset completed - Extend successful change password statement to “base.html”
    # Profile – Profile management page

    path('register/', user_register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', user_profile_view, name='profile'),
]
