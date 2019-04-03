from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
# This is used to handle all the pages inside Tradable

def home_view(request, *args, **kwargs):
    return redirect('listitem')

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})

def myprofile_view(request, *args, **kwargs):
    return render(request, "myprofile.html", {})
	
def help_view(request, *args, **kwargs):
	return render(request, "help.html")

def contact_view(request, *args, **kwargs):
	return render(request, "contact.html")

def blank_view(request, *args, **kwargs):
	return render(request, "blank.html")