
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:pk>/', consumers.ChatConsumer.as_asgi()),
    path('ws/home/<int:pk>/', consumers.HomeConsumer.as_asgi()),

]
