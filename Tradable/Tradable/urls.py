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
from django.urls import path, include
from pages.views import home_view, about_view, myprofile_view, contact_view, help_view, blank_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about_view, name='about'),
	path('help/', help_view, name='help'),
	path('contact/',contact_view, name='contact'),
    path('myprofile/', myprofile_view, name='myprofile'),
    path('items/', include('items.urls')),
    path('about:blank/', blank_view, name='blank'),
    path('users/', include('users.urls')),
    path('messages/', include('chat.urls', namespace="messages")),
	path('', home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
