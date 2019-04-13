from django.contrib import admin

# Register your models here.
from .models import Item, DescriptionPhoto


class DescriptionPhoto(admin.TabularInline):
    model = DescriptionPhoto


class ItemAdmin(admin.ModelAdmin):
    inlines = [DescriptionPhoto]

    class Meta:
        model = Item


admin.site.register(Item, ItemAdmin)
