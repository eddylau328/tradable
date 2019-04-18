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


class InboxConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Inbox connected", event)
        me = self.scope['user']
        inbox_room = me.username
        self.inbox_room = inbox_room
        await self.channel_layer.group_add(
            inbox_room,
            self.channel_name
        )
        chatroomList = await self.get_chatroom(me)
        msgList = []
        for obj in chatroomList:
            msg = await self.get_msg(obj)
            msgList.append(msg)

        newlist = []
        # print(msgList)
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

        await self.send({
            "type": "websocket.accept"
        })

        await self.send({
            "type": "websocket.send",
            "text": json.dumps(newlist)
        })

    @receiver(post_save, sender=Thread)
    def update_inbox(sender, instance, **kwargs):
        channel_layer = get_channel_layer()
        room1 = instance.first.username
        room2 = instance.second.username
        user1 = instance.first
        user2 = instance.second
        chatroomList1 = Thread.objects.by_user(user1)
        chatroomList2 = Thread.objects.by_user(user2)
        msgList1 = []
        msgList2 = []
        for obj in chatroomList1:
            msg = get_msg_out(obj)
            msgList1.append(msg)
        newlist1 = []
        count = 0
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
            newlist1.append(chatroomDict2)

        async_to_sync(channel_layer.group_send)(
            room1,
            {
                "type": "websocket.send",
                "text": json.dumps(newlist1)
            })

        async_to_sync(channel_layer.group_send)(
            room2,
            {
                "type": "websocket.send",
                "text": json.dumps(newlist2)
            })

    @receiver(post_save, sender=ChatMessage)
    def update_inbox_msg(sender, instance, **kwargs):
        channel_layer = get_channel_layer()
        room1 = instance.thread.first.username
        room2 = instance.thread.second.username
        user1 = instance.thread.first
        user2 = instance.thread.second
        chatroomList1 = Thread.objects.by_user(user1)
        chatroomList2 = Thread.objects.by_user(user2)
        msgList1 = []
        msgList2 = []
        for obj in chatroomList1:
            msg = get_msg_out(obj)
            msgList1.append(msg)
        newlist1 = []
        count = 0
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
            newlist1.append(chatroomDict2)

        async_to_sync(channel_layer.group_send)(
            room1,
            {
                "type": "websocket.send",
                "text": json.dumps(newlist1)
            })

        async_to_sync(channel_layer.group_send)(
            room2,
            {
                "type": "websocket.send",
                "text": json.dumps(newlist2)
            })

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_chatroom(self, user):
        return Thread.objects.by_user(user)

    @database_sync_to_async
    def get_msg(self, thread):
        try:
            msg = ChatMessage.objects.filter(thread=thread)
            latestmsg = msg.latest('id').message
            return latestmsg
        except ChatMessage.DoesNotExist:
            return ""


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Chat connected", event)

        other_user = self.scope['url_route']['kwargs']['username']
        itemID = self.scope['url_route']['kwargs']['itemID']
        me = self.scope['user']
        # print(other_user, me)
        thread_obj = await self.get_thread(me, other_user, itemID)
        print(me, thread_obj.id)
        self.thread_obj = thread_obj
        print(self.thread_obj)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

        last_offer = await self.get_latest_offer(me, thread_obj)
        if last_offer is not None:
            myOfferResponse = {
                'offermessage': str(last_offer),
            }
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(myOfferResponse)
            })

        last_seller_offer = await self.get_latest_seller_offer(thread_obj.item.seller, thread_obj)
        if last_seller_offer is not None:
            myOfferResponse = {
                'offerAccept': last_seller_offer,
            }
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(myOfferResponse)
            })
        # print(thread_obj)

    async def websocket_receive(self, event):
        # when a message is receiverd from the websocket
        print("receive", event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            if (msg is not None):
                user = self.scope['user']
                username = 'default'
                if user.is_authenticated:
                    username = user.username
                myResponse = {
                    'message': msg,
                    'username': username
                }

                await self.create_chat_message(user, msg)

                # broadcasts the message event to be sent
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "chat_message",
                        "text": json.dumps(myResponse)
                    }
                )
            offer = loaded_dict_data.get('offermessage')
            if (offer is not None):
                user = self.scope['user']
                username = 'default'
                if user.is_authenticated:
                    username = user.username
                myOfferResponse = {
                    'offermessage': offer,
                }

                await self.create_offer_message(user, offer)
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "offer_message",
                        "text": json.dumps(myOfferResponse)
                    }
                )
            offerAccept = loaded_dict_data.get('offerAccept')
            if (offerAccept is not None):
                user = self.scope['user']
                username = 'default'
                if user.is_authenticated:
                    username = user.username
                myOfferResponse = {
                    'offerAccept': offerAccept,
                }

                await self.create_offer_message(user, offerAccept)
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        "type": "offer_message",
                        "text": json.dumps(myOfferResponse)
                    }
                )
    # custome

    async def chat_message(self, event):
        # send the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def offer_message(self, event):
        # send the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        # when the socket connects
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_username, itemID):
        return Thread.objects.get_or_new(user, other_username, itemID)[0]

    @database_sync_to_async
    def create_chat_message(self, me, msg):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)

    @database_sync_to_async
    def create_offer_message(self, me, offer):
        thread_obj = self.thread_obj
        if isinstance(offer, bool):
            return OfferMessage.objects.create(thread=thread_obj, user=me, offerAccept=offer)
        else:
            return OfferMessage.objects.create(thread=thread_obj, user=me, offer=offer)

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

    @database_sync_to_async
    def get_latest_seller_offer(self, seller, thread):
        offerList = OfferMessage.objects.filter(thread=thread, user=seller)
        if offerList.exists():
            latestSellerOffer = offerList.latest('id')
            return latestSellerOffer.offerAccept
        else:
            return None


def get_msg_out(thread):
    try:
        msg = ChatMessage.objects.filter(thread=thread)
        latestmsg = msg.latest('id').message
        return latestmsg
    except ChatMessage.DoesNotExist:
        return ""
