from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image

# Create your models here.
# Item model to store all uploaded item from user


class Item(models.Model):
    # It saves the name of the product or the post.
    name = models.CharField(max_length=100, default=None, null=False)
    # It saves the description submitted by the seller. To let other users to understand what the product is.
    description = models.TextField(default=None, null=False)
    # It saves the price of the product set by the seller.
    price = models.DecimalField(decimal_places=2, max_digits=10000, default=None, null=False)
    # It saves the condition description of the product.
    condition = models.TextField(default=None, null=False)
    # It saves the time that the item is created.
    createdDateTime = models.DateTimeField(default=timezone.now)
    # It saves the seller as a user object.
    # if the sellor account is deleted, the item posts will be deleted
    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    # It saves the photo which is used to display when it is showed in the item_list_view.
    displayPhoto = models.ImageField(upload_to='item_pics', blank=False, null=True)
    # It saves the availability of the product which means that whether it is already sold or not.
    isSoldOut = models.BooleanField(default=False)

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
    # It saves the corresponding item to this description photo object.
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # It saves the photo submitted by the seller.
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
