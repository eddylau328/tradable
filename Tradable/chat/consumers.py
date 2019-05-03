import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage, OfferMessage
from django.contrib.auth.models import User
from items.models import Item
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# InboxConsumer is a websocket for inbox page
# The target is to update whenever any msg is sent or chatroom is created


class InboxConsumer(AsyncConsumer):
    # things that when the websocket connect
    async def websocket_connect(self, event):
        print("Inbox connected", event)
        me = self.scope['user']
        inbox_room = me.username
        self.inbox_room = inbox_room
        # create a channel layer at redis server for sending information
        await self.channel_layer.group_add(
            inbox_room,
            self.channel_name
        )
        # Here is making a list that contains all the chatrooms that one user have
        chatroomList = await self.get_chatroom(me)
        msgList = []
        for obj in chatroomList:
            msg = await self.get_msg(obj)
            msgList.append(msg)

        newlist = []
        count = 0
        for obj in chatroomList:
            chatroomDict = {
                'firstusername': obj.first.username,
                'secondusername': obj.second.username,
                'itemname': obj.item.name,
                'threadid': obj.id,
                'itemid': obj.item.id,
                'firstuserpic': obj.first.profile.image.url,
                'seconduserpic': obj.second.profile.image.url,
                'msg': msgList[count]
            }
            count = count + 1
            newlist.append(chatroomDict)

        # it is needed for the websocket to accept the connection
        await self.send({
            "type": "websocket.accept"
        })

        # When it is first connected update the current inbox to prevent any update when loading the page
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(newlist)
        })

    # receiver function can be called when a Thread object is created
    @receiver(post_save, sender=Thread)
    def update_inbox(sender, instance, **kwargs):
        # Here is making two list that contains all the chatrooms that one user have
        channel_layer = get_channel_layer()
        room1 = instance.first.username
        room2 = instance.second.username
        user1 = instance.first
        user2 = instance.second
        # List1 and List2 are prepared to send to the users involved in the chatroom
        chatroomList1 = Thread.objects.by_user(user1)
        chatroomList2 = Thread.objects.by_user(user2)
        msgList1 = []
        msgList2 = []
        for obj in chatroomList1:
            msg = get_msg_out(obj)
            msgList1.append(msg)
        newlist1 = []
        count = 0
        # organise the data into a dictionary format
        for obj in chatroomList1:
            chatroomDict1 = {
                'firstusername': obj.first.username,
                'secondusername': obj.second.username,
                'itemname': obj.item.name,
                'threadid': obj.id,
                'itemid': obj.item.id,
                'firstuserpic': obj.first.profile.image.url,
                'seconduserpic': obj.second.profile.image.url,
                'msg': msgList1[count]
            }
            count = count + 1
            newlist1.append(chatroomDict1)

        for obj in chatroomList2:
            msg = get_msg_out(obj)
            msgList2.append(msg)
        newlist2 = []
        count = 0
        # organise the data into a dictionary format
        for obj in chatroomList2:
            chatroomDict2 = {
                'firstusername': obj.first.username,
                'secondusername': obj.second.username,
                'itemname': obj.item.name,
                'threadid': obj.id,
                'itemid': obj.item.id,
                'firstuserpic': obj.first.profile.image.url,
                'seconduserpic': obj.second.profile.image.url,
                'msg': msgList2[count]
            }
            count = count + 1
            newlist2.append(chatroomDict2)

        # send to the first user in the chatroom
        async_to_sync(channel_layer.group_send)(
            room1,
            {
                "type": "inbox_data",
                "text": json.dumps(newlist1)
            })

        # send to the second user in the chatroom
        async_to_sync(channel_layer.group_send)(
            room2,
            {
                "type": "inbox_data",
                "text": json.dumps(newlist2)
            })

    # receiver function can be called when a message object is created
    @receiver(post_save, sender=ChatMessage)
    def update_inbox_msg(sender, instance, **kwargs):
        channel_layer = get_channel_layer()
        room1 = instance.thread.first.username
        room2 = instance.thread.second.username
        user1 = instance.thread.first
        user2 = instance.thread.second
        # Here is making two list that contains all the chatrooms that one user have
        chatroomList1 = Thread.objects.by_user(user1)
        chatroomList2 = Thread.objects.by_user(user2)
        msgList1 = []
        msgList2 = []
        for obj in chatroomList1:
            msg = get_msg_out(obj)
            msgList1.append(msg)
        newlist1 = []
        count = 0
        # organise the data into a dictionary format
        for obj in chatroomList1:
            chatroomDict1 = {
                'firstusername': obj.first.username,
                'secondusername': obj.second.username,
                'itemname': obj.item.name,
                'threadid': obj.id,
                'itemid': obj.item.id,
                'firstuserpic': obj.first.profile.image.url,
                'seconduserpic': obj.second.profile.image.url,
                'msg': msgList1[count]
            }
            count = count + 1
            newlist1.append(chatroomDict1)

        for obj in chatroomList2:
            msg = get_msg_out(obj)
            msgList2.append(msg)
        newlist2 = []
        count = 0
        # organise the data into a dictionary format
        for obj in chatroomList2:
            chatroomDict2 = {
                'firstusername': obj.first.username,
                'secondusername': obj.second.username,
                'itemname': obj.item.name,
                'threadid': obj.id,
                'itemid': obj.item.id,
                'firstuserpic': obj.first.profile.image.url,
                'seconduserpic': obj.second.profile.image.url,
                'msg': msgList2[count]
            }
            count = count + 1
            newlist2.append(chatroomDict2)

        # send to the first user in the chatroom
        async_to_sync(channel_layer.group_send)(
            room1,
            {
                "type": "inbox_data",
                "text": json.dumps(newlist1)
            })

        # send to the second user in the chatroom
        async_to_sync(channel_layer.group_send)(
            room2,
            {
                "type": "inbox_data",
                "text": json.dumps(newlist2)
            })

    # create a function for sending the chatroom list
    async def inbox_data(self, event):
        # send the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    # websocket receive
    async def websocket_receive(self, event):
        print("receive", event)

    # websocket disconnect
    async def websocket_disconnect(self, event):
        print("disconnected", event)

    # finding the thread object by user object
    @database_sync_to_async
    def get_chatroom(self, user):
        return Thread.objects.by_user(user)

    # finding the message object by thread object and return the string
    @database_sync_to_async
    def get_msg(self, thread):
        try:
            msg = ChatMessage.objects.filter(thread=thread)
            latestmsg = msg.latest('id').message
            return latestmsg
        except ChatMessage.DoesNotExist:
            return ""


class ChatConsumer(AsyncConsumer):
    # websocket connect
    async def websocket_connect(self, event):
        print("Chat connected", event)

        other_user = self.scope['url_route']['kwargs']['username']
        itemID = self.scope['url_route']['kwargs']['itemID']
        me = self.scope['user']
        # Get the thread object
        thread_obj = await self.get_thread(me, other_user, itemID)
        self.thread_obj = thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        # create a channel in redis server for sending the message
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        # it is needed for websocket to accept the connection
        await self.send({
            "type": "websocket.accept"
        })
        # get the latest offer from all the message object in this thread
        last_offer = await self.get_latest_offer(me, thread_obj)
        if last_offer is not None:
            myOfferResponse = {
                'offermessage': str(last_offer),
            }
            # send it to the frontend
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(myOfferResponse)
            })

        # get the latest offer from all the message object in this thread
        last_seller_offer = await self.get_latest_seller_offer(thread_obj.item.seller, thread_obj)
        if last_seller_offer is not None:
            myOfferResponse = {
                'offerAccept': last_seller_offer,
            }
            # send it to the frontend
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(myOfferResponse)
            })

    # websocket receive
    async def websocket_receive(self, event):
        # when a message is receiverd from the websocket
        print("receive", event)
        # get the data sent from the frontend socket
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            # if the sent data consists of message
            if (msg is not None):
                user = self.scope['user']
                username = 'default'
                if user.is_authenticated:
                    username = user.username
                myResponse = {
                    'message': msg,
                    'username': username
                }
                # create the message
                await self.create_chat_message(user, msg)
                # broadcasts the message event to be sent
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "chat_message",
                        "text": json.dumps(myResponse)
                    }
                )

        # if the sent data consists of offer message
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            offer = loaded_dict_data.get('offermessage')
            if (offer is not None):
                user = self.scope['user']
                username = 'default'
                if user.is_authenticated:
                    username = user.username
                myOfferResponse = {
                    'offermessage': offer,
                }
                # create a offer message which is assigning the offerPrice
                await self.create_offer_message(user, offer)
                # send the offer message to seller
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "offer_message",
                        "text": json.dumps(myOfferResponse)
                    }
                )

        # if the sent data consists of offer message from seller (Accept/Reject)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            offerAccept = loaded_dict_data.get('offerAccept')
            if (offerAccept is not None):
                user = self.scope['user']
                itemID = self.scope['url_route']['kwargs']['itemID']
                other_user = self.scope['url_route']['kwargs']['username']
                thread_obj = await self.get_thread(user, other_user, itemID)
                last_offer = await self.get_latest_offer(user, thread_obj)
                if last_offer is not None:
                    username = 'default'
                    if user.is_authenticated:
                        username = user.username
                    myOfferResponse = {
                        'offerAccept': offerAccept,
                    }
                    # create a offer message which is assigning the offer accept/reject
                    await self.create_offer_message(user, offerAccept)
                    # send the update message to buyer
                    await self.channel_layer.group_send(
                        self.chat_room,
                        {
                            "type": "offer_message",
                            "text": json.dumps(myOfferResponse)
                        }
                    )

    # create a function for sending the message
    async def chat_message(self, event):
        # send the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    # create a function for sending the offer message
    async def offer_message(self, event):
        # send the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    # websocket disconnect
    async def websocket_disconnect(self, event):
        # when the socket connects
        print("disconnected", event)

    # finding the thread object by first username, second username and item ID
    # as these three fields forms a unique thread object
    @database_sync_to_async
    def get_thread(self, user, other_username, itemID):
        return Thread.objects.get_or_new(user, other_username, itemID)[0]

    # function for create a chat message
    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)

    # function for create a offer message
    @database_sync_to_async
    def create_offer_message(self, me, offer):
        thread_obj = self.thread_obj
        if isinstance(offer, bool):
            return OfferMessage.objects.create(thread=thread_obj, user=me, offerAccept=offer)
        else:
            return OfferMessage.objects.create(thread=thread_obj, user=me, offer=offer)

    # finding the latest offer in all the message objects inside the thread object
    @database_sync_to_async
    def get_latest_offer(self, me, thread):

        offerList = OfferMessage.objects.filter(thread=thread).exclude(user=thread.item.seller)
        if offerList.exists():
            latestOfferMessage = offerList.latest('id')
            if latestOfferMessage.offerDelete is not None:
                return latestOfferMessage.offerDelete
            else:
                return latestOfferMessage.offer
        else:
            return None

    # finding the latest offer(Accept/Reject) in all the message objects inside the thread object
    @database_sync_to_async
    def get_latest_seller_offer(self, seller, thread):
        offerList = OfferMessage.objects.filter(thread=thread, user=seller)
        if offerList.exists():
            latestSellerOffer = offerList.latest('id')
            return latestSellerOffer.offerAccept
        else:
            return None

# Function that can be called within this program
# Receiver function cannot use async function therefore they cannot call async function
# finding the message object by thread object and return the string
def get_msg_out(thread):
    try:
        msg = ChatMessage.objects.filter(thread=thread)
        latestmsg = msg.latest('id').message
        return latestmsg
    except ChatMessage.DoesNotExist:
        return ""
