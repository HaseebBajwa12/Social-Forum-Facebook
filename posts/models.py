import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.utils import timezone

from user_management.models import User


def upload_post_image(instance, filename):
    return "posts/{filename}".format(filename=filename)


class Post(models.Model):
    author = models.ForeignKey(User, related_name="user_post", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True)
    choices = [("public", "Public"), ("only_me", "Only Me"), ("only_friends", "Friends Only")]
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikes")
    privacy = models.CharField(max_length=30, choices=choices)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="posts", default="posts/zoobie_ape.jpg")


class Media(models.Model):
    post = models.ForeignKey(Post, related_name="post_media", on_delete=models.CASCADE, null=True, blank=True)
    media_type = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# class PostLike(models.Model):
#     user = models.ForeignKey(User, related_name="post_liker", on_delete=models.CASCADE, null=True, blank=True)
#     post = models.ForeignKey(Post, related_name="liked_post", on_delete=models.CASCADE, null=True, blank=True)
#     status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="comment_dislikes")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="+")

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by("-created_at").all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class Image(models.Model):
    image = models.ImageField(upload_to='posts/post_photos', blank=True, null=True)


class Notification(models.Model):
    # 1 = Like, 2 = Comment
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name="notification_from", on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
    description = models.CharField(max_length=500)
    url = models.URLField()
    seen = models.BooleanField(default=False)

    def save(self, *args, **kargs):
        super().save(*args, **kargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "room_1",
            {
                'type': 'send_notification',
                'value': {
                    "from_user": self.from_user.username,

                    "url": self.url,
                    "description": self.description,
                    "notification_type":self.notification_type,

                }
            }
        )

        print("saved function called")


# class Notificationsss(models.Model):
#     user = models.ForeignKey(User, related_name='user_notification', on_delete=models.CASCADE)
#     description = models.CharField(max_length=500)
#     url = models.URLField()
#     seen = models.BooleanField(default=False)
#     liker = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+", blank=True, null=True)


