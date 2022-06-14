# import json
#
# from channels.auth import get_user
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.db.models import Q
# from user_management.models import User
# from notification.models import Notifications, NotificationThread
#
#
# @sync_to_async
# def ConnetUser(pk):
#     user = User.objects.get(pk=pk)
#     user.is_online = True
#     user.save()
#
#
# @sync_to_async
# def DisConnetUser(pk):
#     user = User.objects.get(pk=pk)
#     user.is_online = False
#     user.save()
#
#
# class HomeConsumer(AsyncWebsocketConsumer, object):
#     # async def connect(self):
#     #     print("DSFfffffffff")
#     #     self.user_id = self.scope['url_route']['kwargs']['pk']
#     #     print("user", self.user_id)
#     #     self.notify_group_name = 'notify_%d' % self.user_id
#     #     print(self.notify_group_name)
#     #
#     #     await self.channel_layer.group_add(
#     #         self.notify_group_name,
#     #         self.channel_name,
#     #
#     #     )
#     #     await self.accept()
#     #     print("sfgdnhhhhhhhhhhhhhhhh")
#     #     await self.send(text_data=json.dumps({'status': 'connected from django channels'}))
#     #     print("asdfghj")
#
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(args, kwargs)
#     #     self.thread = None
#     #     self.room_name = None
#     #     self.user1 = None
#     #     self.user2 = None
#     #     print("call 19")
#
#     async def connect(self):
#         print("connecting")
#         # self.user1 = await self.get_usermodel(id=1)  # await get_user(self.scope)
#         self.user1 = await get_user(self.scope['user'])
#         print("scope is", self.scope)
#         user2_pk = self.scope['url_route']['kwargs']['pk']
#         self.user2 = await self.get_usermodel(pk=user2_pk)
#         # if not self.user1.is_authenticated:
#         #     await self.close()
#
#         self.thread = await self.get_thread()
#         self.room_name = f"chat_room_{self.thread.id}"
#         await self.channel_layer.group_add(
#             self.room_name,
#             self.channel_name
#         )
#         await self.accept()
#         print("connected")
#
#     async def disconnect(self, close_code):
#         # Leave room
#         await self.channel_layer.group_discard(
#             self.room_name,
#             self.channel_name
#         )
#
#         # async def receiver(self, event):
#         #     notify = event.get("notify" or None)
#         #     print("notify",notify)
#         #     request_pk = event.get("request_pk" or None)
#         #     notify_delete = event.get("notify_delete" or None)
#         #     request_delete = event.get("request_delete" or None)
#         #     notification = event.get("notification" or None)
#         #     print(notification)
#         #     # Send message to WebSocket
#         #     await self.send(text_data=json.dumps(
#         #         {'notify': notify, 'request_pk': request_pk, 'notify_delete': notify_delete,
#         #          "request_delete": request_delete, 'notification': notification, }))
#
#         # async def receive(self, text_data):
#         #     print("received call")
#         #     text_data_json = json.loads(text_data)
#         #     print(text_data_json)
#         #     data = self.get_notificationmodel()
#         #     print(data)
#
#         # notification = text_data_json['notification']
#         # record = {
#         #     "sender_id": self.from_user.id,
#         #     "receiver_id": self.to_user.id,
#         #     "notification": notification,
#         #     "thread_id": self.thread.id
#         # }
#         # latest_notification = await self.create_notification(**record)
#         # saved_message = {
#         #     "id": latest_notification.id,
#         #     "sender": await self.get_full_name(self.from_user),
#         #     "sender_id": self.from_user.id,
#         #     "receiver": await self.get_full_name(self.to_user),
#         #     "message": latest_notification.message,
#         #     "created_at": f'{latest_notification.created_at.date()} - {str(latest_notification.created_at.time())[:8]}'
#         # }
#         # await self.channel_layer.group_send(
#         #     self.notify_group_name,
#         #     {
#         #         'type': 'send_new_notification',
#         #         'value': text_data_json
#         #     }
#         # )
#
#     async def send_new_notification(self, event):
#         print("inisde of function")
#         await self.send(text_data=json.dumps(event.get('value')))
#
#     @database_sync_to_async
#     def create_notification(self, **kwargs):
#         return Notifications.objects.create(**kwargs)
#
#     @database_sync_to_async
#     def get_full_name(self, instance):
#         return f"{instance.first_name} {instance.last_name}"
#
#     @database_sync_to_async
#     def get_notificationmodel(self, **kwargs):
#         return Notifications.objects.get(**kwargs)
#
#     @database_sync_to_async
#     def get_usermodel(self, **kwargs):
#         return User.objects.get(**kwargs)
#
#     @database_sync_to_async
#     def get_thread(self):
#         threads = NotificationThread.objects.filter(
#             Q(sender=self.user1) & Q(receiver=self.user2) |
#             Q(sender=self.user2) & Q(receiver=self.user1)
#         )
#         if threads.count() > 0:
#             return threads.first()
#         else:
#             thread = NotificationThread(sender=self.user1, receiver=self.user2, last_updated=timezone.now())
#             thread.save()
#             return thread

import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer

# @receiver(post_save, sender=Notification)
# def post_handler(sender, created, **kwargs):
#     """
#     This signal is called when create or update operation
#     is performed from admin site on KeywordTag model.
#     """
#     if created:
#         print(**kwargs)
#
from user_management.models import User
from posts.models import Notification


class NotificationConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None

    def connect(self):
        print("connecting")
        # self.user1 = await get_user(self.scope)
        # if not self.user1.is_authenticated:
        #     await self.close()

        self.room_name = "room_1"  # {self.user1.id}
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        self.accept()
        print("connected")

    def disconnect(self, close_code):
        # Remove the room name to channel layer
        self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        print("disconnected")

    def receive(self, text_data):
        print("received call")
        text_data_json = json.loads(text_data)
        print(text_data_json)
        self.send(text_data=json.dumps(text_data_json))

    def send_notification(self, event):
        print("send notification called")
        self.send(text_data=json.dumps(event.get('value')))

    def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        print("chat_message")
        self.send(text_data=event["text"])

    # @database_sync_to_async
    # def count_notification(self):
    #     notification_obj = Notification.objects.filter(seen=False).count()
    #     self.send(text_data=json.dumps(notification_obj))
