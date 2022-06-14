

from django.urls import path

from . import views
from .views import index, chat_thread,UserSearch

app_name = "chatapp"
urlpatterns = [
    # path('', views.chat_header, name='chat-list'),
    # path("chat/<int:tid>/", views.chat_header, name="chat-detail"),
    # path("chat_page/",views.chat_page,name="chat-page")
    path('chat/', index, name="chat-page"),
    path('chat/<int:pk>/', chat_thread, name="messages"),
    path('user/',UserSearch.as_view(),name="user-search"),
    path('notify/', views.NotifyHref, name="notify"),

]
