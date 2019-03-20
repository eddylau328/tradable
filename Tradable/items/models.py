from django.db import models

# Create your models here.
# Item model to store all uploaded item from user
class Item(models.Model):
	name            = models.CharField( max_length = 100)
	description     = models.TextField()
	price           = models.DecimalField(decimal_places=2, max_digits=10000)
	condition       = models.TextField()
	createdDateTime = models.DateTimeField(auto_now=True)