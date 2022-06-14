# from django.shortcuts import render
#
# from .models import Thread
#
# from django.db.models import F, Q
#
# # Create your views here.
#
# from user_management.models import User
#
# from chat.models import Chat

#
# def chat_header(request, tid=None):
#     user_id = 1
#     threads = Thread.objects.filter(Q(user1_id=1) | Q(user2_id=1)).order_by("-id")
#     result = []
#     for thread in threads:
#         chat = Chat.objects.filter(thread=thread).order_by("-timestamp")[0]
#         result.append({
#             "user": thread.user2 if thread.user2 != user_id else thread.user2,
#             "message": chat.message,
#             "time": chat.timestamp,
#             "thread_id": thread.id,
#         })
#     _tid = tid if tid is not None else result[0]["thread_id"]
#     messages = Chat.objects.filter(thread_id=tid)
#     return render(request, "chat.html", context={"result": result, "messages": messages})
#
#
# def chat_details(request, tid):
#     messages = Chat.objects.filter(thread_id=tid)
#     context = {"messages": messages}
#     return render(request, "chat.html", context=context)
#
#
# def chat_page(request):
#     return render(request,'chat.html')


# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View

from .models import Thread, Chat
from datetime import datetime
from user_management.models import User
from posts.models import Notification, Post


# Django Channels


@login_required
def index(request):
    # thread_obj = Thread.objects.filter().first()
    # receiver = thread_obj.receiver
    threads = Thread.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    header = []
    for thread in threads:
        message_thread = thread.chat_thread.all()

        last_message = message_thread[0].message if message_thread.count() > 0 else "..."
        header.append(
            {
                "id": thread.id,
                "user": thread.sender if thread.sender != request.user else thread.receiver,
                "message": last_message,
            }
        )
    context = {
        "header": header,
        "chat": []
    }
    return render(request, 'chat.html', context)


def NotifyHref(request, pk):
    notify = get_object_or_404(Notification, pk=pk)
    return render(request,"post_list.html",{'notify':notify})


@login_required
def chat_thread(request, pk):
    threads = Thread.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    print(request.user)
    header = []
    for thread in threads:
        last_message = thread.chat_thread.all().order_by("created_at").last()
        header.append(
            {
                "id": thread.id,
                "user": thread.sender if thread.sender != request.user else thread.receiver,
                "message": last_message.message if last_message is not None else "...",
            }
        )
    user2 = Thread.objects.get(pk=pk)
    context = {
        "header": header,
        "chat": Chat.objects.filter(thread_id=pk),
        "user2": user2.sender.id if user2.sender != request.user else user2.receiver.id
    }

    return render(request, 'chat.html', context)


def test(request, pk):
    return render(request, "test.html")


def home(request):
    return render(request, 'home.html')


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        print("query", query)
        user_list = User.objects.filter(Q(username__icontains=query))
        context = {
            "user_list": user_list,
        }
        return render(request, "chat.html", context)
