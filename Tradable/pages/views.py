from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# This is used to handle all the pages inside Tradable

def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})

def myprofile_view(request, *args, **kwargs):
    return render(request, "myprofile.html", {})