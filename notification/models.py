# from django.db import models
# from django.utils import timezone
#
# from posts.models import Comment, Post
# from user_management.models import User
#
#
# # class Notification(models.Model):
# #     # 1 = Like, 2 = Comment
# #     notification_type = models.IntegerField()
# #     to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
# #     from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null=True)
# #     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
# #     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
# #     date = models.DateTimeField(default=timezone.now)
# #     user_has_seen = models.BooleanField(default=False)
#
#
# # class Notification_Sender_Receiver(models.Model):
# #     sender = models.ForeignKey(User, on_delete=models.CASCADE)
# #     receiver = models.ForeignKey(User, on_delete=models.CASCADE)
# #
# #
# # class Notifications(models.Model):
# #     NOTIFICATION_TYPES = (
# #         (1, 'Likes'), (2, 'comment'))
# #     # 1 = Like, 2 = Comment
# #     notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
# #     description = models.CharField(max_length=200)
# #     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
# #     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
# #     user_has_seen = models.BooleanField(default=False)
# #     notification= models.ForeignKey(Notification_Sender_Receiver, related_name="",
# #                                         on_delete=models.CASCADE)
# #
# #
# # class NotificationThread(models.Model):
# #     sender = models.ForeignKey(User, related_name='noti_sender', on_delete=models.PROTECT)
# #     receiver = models.ForeignKey(User, related_name='noti_receiver', on_delete=models.PROTECT)
# #     last_updated = models.DateTimeField()
# #
# #     class Meta:
# #         unique_together = ('sender', 'receiver')
# #         ordering = ('-last_updated',)
# #
# #     def __str__(self):
# #         return f"{self.sender.username} : {self.receiver.username}"
# #
# #
# # class Notifications(models.Model):
# #     NOTIFICATION_TYPES = (
# #         (1, 'Likes'), (2, 'comment'))
# #     # 1 = Like, 2 = Comment
# #     notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
# #     to_user = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE, null=True)
# #     from_user = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
# #     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
# #     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
# #     date = models.DateTimeField(default=timezone.now)
# #     user_has_seen = models.BooleanField(default=False)
# #     thread = models.ForeignKey(NotificationThread, on_delete=models.CASCADE)
