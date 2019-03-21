from django.db import models

# Create your models here.
# User model to store all registered user profile
class User(models.Model):
	user_name        = models.CharField( max_length = 100)
	userID = models.BigIntegerField()
	user_email       = models.EmailField(max_length=254)