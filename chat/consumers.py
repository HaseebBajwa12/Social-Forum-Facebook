import json

from channels.auth import get_user
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

# from user_management.models import User
from django.db.models import Q
from django.utils import timezone
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Thread, Chat
from posts.models import Notification
from posts.models import Post
from user_management.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user1 = await get_user(self.scope)
        # self.user1 = await self.get_usermodel(pk=1)
        print("get  user", self.user1.id)
        print("scope is", self.scope)
        user2_pk = self.scope['url_route']['kwargs']['pk']
        self.user2 = await self.get_usermodel(pk=user2_pk)
        print("model  user", self.user2)
        # if not self.user1.is_authenticated:
        #     await self.close()

        self.thread = await self.get_thread()
        self.room_name = f"chat_room_{self.thread.id}"
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()
        print("chat module connected ")

    async def disconnect(self, close_code):
        # Remove the room name to channel layer
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        print("disconnected")

    async def receive(self, text_data):
        print("received call")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        record = {
            # "sender_id": self.user1.id,
            # "receiver_id": self.user2.id,
            # "message": message,
            # "thread_id": self.thread.id,
            "sender_id":self.user1.id,
            "receiver_id":self.user2.id,
            "message":message,
            "thread_id":self.thread.id,
        }
        # latest_message = await self.create_chat(**record)
        # saved_message = {
        #     "id": latest_message.id,
        #     "sender": await self.get(self.user1),
        #     "sender_id": self.user1.id,
        #     "receiver": await self.get(self.user2),
        #     "message": latest_message.message,
        #     "created_at": f'{latest_message.created_at.date()} - {str(latest_message.created_at.time())[:8]}'
        # }
        # await self.channel_layer.group_send(
        #     self.room_name,
        #     {
        #         'type': 'send_messages',
        #         'value': saved_message
        #     }
        # )
        lastest_message = await self.create_chat(**record)
        saved_message = {
            "id": lastest_message.id,
            "sender": await self.get_full_name(self.user1),
            "sender_id": self.user1.id,
            "receiver": await self.get_full_name(self.user2),
            "message": lastest_message.message,
            "created_at": f'{lastest_message.created_at.date()}-{str(lastest_message.created_at.time())[:8]}'

        }
        print(saved_message)
        await self.channel_layer.group_send(
            self.room_name, {
                "type": "send_new_messages",
                "value": saved_message,
            }
        )

    async def chat_message(self, event):
        message = event.get('message') if event.get('message') else None

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,

        }))

    async def send_new_messages(self, event):
        await self.send(text_data=json.dumps(event.get('value')))

    @database_sync_to_async
    def get_usermodel(self, **kwargs):
        return User.objects.get(**kwargs)

    @database_sync_to_async
    def get_thread(self):
        threads = Thread.objects.filter(
            Q(sender=self.user1) & Q(receiver=self.user2) |
            Q(sender=self.user2) & Q(receiver=self.user1)
        )
        if threads.count() > 0:
            return threads.first()
        else:
            thread = Thread(sender=self.user1, receiver=self.user2, last_updated=timezone.now())
            thread.save()
            return thread

    @database_sync_to_async
    def create_chat(self, **kwargs):
        return Chat.objects.create(**kwargs)

    @database_sync_to_async
    def get_full_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class HomeConsumer(AsyncWebsocketConsumer, object):

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['pk']
        print(self.user_id)
        self.notify_group_name = 'notify_%d' % self.user_id
        print(self.notify_group_name)
        # if not self.user_id.is_authenticated:
        #     await self.close()
        # Join room
        await self.channel_layer.group_add(
            self.notify_group_name,
            self.channel_name
        )

        await self.accept()



    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.notify_group_name,
            self.channel_name
        )



    async def chat_message(self, event):
        notify = event.get("notify" or None)
        message = event.get("messages" or None)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {'notify': notify, 'message': message, }))

