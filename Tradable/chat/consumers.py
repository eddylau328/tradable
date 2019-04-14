import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage, OfferMessage
from django.contrib.auth.models import User


class InboxConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Inbox connected", event)
        me = self.scope['user']
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

        await asyncio.sleep(100)
        await self.send({
            "type": "websocket.close"
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
            print(last_offer)
            myOfferResponse = {
                'offermessage': str(last_offer),
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
                    'username': username
                }

                await self.create_offer_message(user, offer)
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

        offerList = OfferMessage.objects.exclude(user=thread.item.seller)
        if offerList.exists():
            latestOfferMessage = offerList.latest('id')
            if latestOfferMessage.offerDelete is not None:
                return latestOfferMessage.offerDelete
            else:
                return latestOfferMessage.offer
        else:
            return None
