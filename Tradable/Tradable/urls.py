"""Tradable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages.views import home_view, about_view, myprofile_view
from items.views import item_list_all_view, item_create_view, item_dynamic_lookup_view
from users.views import user_register_view, user_profile_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('myprofile/', myprofile_view, name='myprofile'),
    path('items/', item_list_all_view, name='item_list_all_view'),
    path('items/create/', item_create_view, name='item_detail_view'),
    path('items/<int:item_id>/', item_dynamic_lookup_view, name='dynamic item view'),
    path('users/register/', user_register_view, name='register'),
    path('users/login/', auth_views.LoginView.as_view(template_name='user_login.html'), name='login'),
    path('users/logout/', auth_views.LogoutView.as_view(template_name='user_logout.html'), name='logout'),
    path('users/profile/', user_profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
