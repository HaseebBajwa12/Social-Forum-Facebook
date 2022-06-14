from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string

channel_layer = get_channel_layer()
from posts.models import Notification


@receiver(post_save, sender=Notification)
def AfterNotifies(sender, instance, **kwargs):
    notify_group_name = 'notify_%d' % instance.receiver.pk
    async_to_sync(channel_layer.group_send)(
        notify_group_name,
        {'type': 'chat_message', 'notify': render_to_string('fragments/nav/notify.html',
                                                            {'notify': instance, 'request.user': instance.receiver})})


@receiver(post_delete, sender=Notification)
def AfterNotifiesDelete(sender, instance, **kwargs):
    notify_group_name = 'notify_%d' % instance.receiver.pk
    async_to_sync(channel_layer.group_send)(
        notify_group_name,
        {'type': 'chat_message', 'notify_delete': instance.pk})
