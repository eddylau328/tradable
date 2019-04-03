from django.contrib import admin

# Register your models here.
from .models import Item, DescriptionPhoto

admin.site.register(Item)
admin.site.register(DescriptionPhoto)
