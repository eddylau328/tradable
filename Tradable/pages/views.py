from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# This is used to handle all the pages inside Tradable

def home_view(*args, **kwargs):
    return HttpResponse("<h1>Home Page</h1>")
