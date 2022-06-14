from django.contrib import admin

# Register your models here.
from posts.models import Post, Comment,Notification

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
