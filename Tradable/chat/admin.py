from django.contrib import admin


from .models import Thread, ChatMessage, OfferMessage


class OfferMessage(admin.TabularInline):
    model = OfferMessage


class ChatMessage(admin.TabularInline):
    model = ChatMessage


#Inline can make OfferMessage & ChatMessage objects inside Thread Object in the admin page
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage, OfferMessage]

    class Meta:
        model = Thread

#Only register Thread and ThreadAdmin, as ThreadAdmin already consist OfferMsg & ChatMsg
admin.site.register(Thread, ThreadAdmin)
