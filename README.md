#CSCI3100 Softwear Enginerering

##Group 33 Tradable

##Description
-todo description

##Prerequisites
###Python 3.7.2
[downlaod](https://pythoninsider.blogspot.com/2019/03/python-3410-is-now-available.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+PythonInsider+%28Python+Insider%29)
###Django 2.1.7 and adds-on
Django:
````
pip install Django==2.1.7
````
Verify:
````
>>> import django
>>> print(django.get_version())
2.1
````
Pillow 5.4.2
````
>pip install Pillow
````
django-crispy-forms 1.7.2
````
>pip install --upgrade django-crispy-forms
````
pywin32 
````
>pip install pywin32 
````
pypwin32
````
>pip install pypwin32
````
channels 2.17
````
>pip install -U channels
````
channels-redis 2.3.3
````
>pip install channels-redis
````
redis 3.2.1
````
>pip install redis
````
Port for Windows based on Redis:
[download](https://github.com/MicrosoftArchive/redis/releases)
###Visual C++
[download](https://support.microsoft.com/zh-hk/help/2977003/the-latest-supported-visual-c-downloads)

#change log(Master Branch)
````
24/3/2019
Initial stage
to be comment
````
```
22/3/2019
Early devlopment stage  
-----------------------------------------------
A very basic framwork is implemented
Implemented funtion:
1# home page 
2# about page
3# my profile 
3# navigator bar
4# user detail database and item detail database
5# create item, list all item and view specific item's detail
6# register and login
-----------------------------------------------
Detail Discription:
The default of templates file is directed to root/templates

App: 'pages'
->the app for the bottom use for our site
->which is currently used for some simple pages like 'about us', 'home', 'my profile'
->webpage is not restricted to be coded in here

App: 'items'
->the app for storing all items detail
->the app can now list all items' name inside the database
->view to browse specific item
->create an item

App: 'Users'
->the app for storing all user detail
->login function is not included at the moment (created)
->dataField for password is not implemented as well (solved)
-----------------------------------------------
todo-task for current developing phase:
->allow data entry from front-end to back-end (done)
->create 'register' app (done)
->create 'login' app (done)
->...
#feel free to add more if any

```
```
13-03-2019
-----------------------------------------------
Projected started
```
