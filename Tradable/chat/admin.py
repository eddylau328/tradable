from django.contrib import admin


from .models import Thread, ChatMessage, OfferMessage


class OfferMessage(admin.TabularInline):
    model = OfferMessage


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage, OfferMessage]

    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
