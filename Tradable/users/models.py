from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Profile is a model that used to save the users description


class Profile(models.Model):
    # OneToOneField can restrict one User to have one Profile
    # on_delete=models.CASCADE, when user is deleted, his/her profile is deleted
    # on_delete=models.CASCADE, when user's profile is deleted, user will not be deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
