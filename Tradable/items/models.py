from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
# Item model to store all uploaded item from user


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    condition = models.TextField()
    createdDateTime = models.DateTimeField(default=timezone.now)
    # if the sellor account is deleted, the item posts will be deleted
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    # QuerySet will show [<Item: <seller> <name> >]
    def __str__(self):
        return f'{self.seller} {self.name}'
