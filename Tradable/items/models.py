from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

# Create your models here.
# Item model to store all uploaded item from user


class Item(models.Model):
    name = models.CharField(max_length=100, default=None, null=False)
    description = models.TextField(default=None, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10000, default=None, null=False)
    condition = models.TextField(default=None, null=False)
    createdDateTime = models.DateTimeField(default=timezone.now)
    # if the sellor account is deleted, the item posts will be deleted
    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    displayPhoto = models.ImageField(upload_to='item_pics', blank=False, null=True)

    # QuerySet will show [<Item: <seller> <name> >]
    def __str__(self):
        return f'{self.seller} {self.name}'

    # overwrite the save method
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.displayPhoto.path)
        # resize profile image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.displayPhoto.path)


class DescriptionPhoto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    photo = models.ImageField(upload_to='item_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.item.seller} {self.item.name}'

        # overwrite the save method
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.photo.path)
        # resize profile image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
