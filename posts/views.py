from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from user_management.models import Profile, User
from .models import Notification
from .models import Comment, Post


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        print("in get function")
        query = self.request.GET.get("query")
        print("query",query)
        profile_list = User.objects.filter(Q(username__icontains=query))
        print(profile_list)
        context = {
            "profile_list": profile_list,
        }
        return render(request, "social/post_list.html", context)



def test(request):
    return render(request, 'posts/test.html')


# def seen_test(request):
#     data = {
#         "from_user_id": 1,
#          "to_user_id":2,
#         "description": "hello world",
#         "url": "https://google.com",
#         "notification_type":1,
#     }
#     Notification.objects.create(**data)
#     return HttpResponse("<h1> notification work successfully")


def view_notification(request, pk):
    pass


def home(request):
    data = {
        'count': 5,
        "notifications": [
            {
                "url": "#",
                "description": "In fact, inserting any fantasy text or a famous text, be it a poem, a speech, "
                               "a literary passage, a song's text, etc., our text generator will provide the random "
                               "extraction of terms and steps to compose your own exclusive Lorem Ipsum.",
                "pk": 4,
                "time_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            },
            {
                "url": "#",
                "description": "In fact, inserting any fantasy text or a famous text, be it a poem, a speech, "
                               "a literary passage, a song's text, etc., our text generator will provide the random "
                               "extraction of terms and steps to compose your own exclusive Lorem Ipsum.",
                "pk": 4,
                "time_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            },
            {
                "url": "#",
                "description": "In fact, inserting any fantasy text or a famous text, be it a poem, a speech, "
                               "a literary passage, a song's text, etc., our text generator will provide the random "
                               "extraction of terms and steps to compose your own exclusive Lorem Ipsum.",
                "pk": 4,
                "time_date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            }
        ]
    }
    render(request, 'home.html', )
