from django.db import models

from django.conf import settings
from django.db import models
from django.db.models import Q
from items.models import Item
from django.db.models.signals import post_save
from django.dispatch import receiver


class ThreadManager(models.Manager):
    # returns a list that contains all the chat rooms that a user has.
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    # returns a chat room that is searched or created with three fields, which are the first user, second user, and the item.
    def get_or_new(self, user, other_username, itemID):  # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username) & Q(item__id=itemID)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username) & Q(item__id=itemID)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            selectedItem = Item.objects.get(id=itemID)
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2,
                    item=selectedItem
                )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    # It saves the first user in this chat.
    first = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    # It saves the second user in this chat.
    second = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    # It saves the latest updated of this chat.
    updated = models.DateTimeField(auto_now=True)
    # It saves the created time of this chat.
    timestamp = models.DateTimeField(auto_now_add=True)
    # It saves the related item of this chat.
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE)
    # It saves the ThreadManager object that provides functions for other usages in view function or web socket function.
    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    # It saves the related thread object.
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    # It saves the user that created the message, which is either first user or second user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    # It saves the message content.
    message = models.TextField()
    # It saves the created time of the message.
    timestamp = models.DateTimeField(auto_now_add=True)


class OfferMessage(models.Model):
    # It saves the related thread object.
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    # It saves the user that created the offer message, which is either first user or second user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    # It saves the money that the buyer wishes to pay.
    offer = models.DecimalField(decimal_places=2, max_digits=10000, default=None, null=True)
    # It saves whether the seller accepts or rejects the offer made by the buyer.
    offerAccept = models.BooleanField(null=True)
    # It saves the created time of the offer message.
    timestamp = models.DateTimeField(auto_now_add=True)


#If the seller accepts the offer made by the buyer, it will create a new offer message with a value of True in offerAccept. And the following function is placed in models.py in the chat app which used to change the related item availability when the seller agreed to sell it to other user.
@receiver(post_save, sender=OfferMessage)
def update_item_isSoldOut(sender, instance, **kwargs):
    if (instance.offerAccept is True):
        searchID = instance.thread.item.id
        Item.objects.filter(id=searchID).update(isSoldOut=True)
