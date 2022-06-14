from django.contrib import admin

# Register your models here.
from chat.models import Chat

from chat.models import Thread

admin.site.register(Chat)
admin.site.register(Thread)