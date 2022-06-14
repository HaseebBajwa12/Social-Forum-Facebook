from django import template

from posts.models import Notification, Post

register = template.Library()


@register.inclusion_tag("notification/show_notifications.html", takes_context=True)
def show_notifications(context):
    request_user = context["request"].user
    notifications = Notification.objects.filter(to_user=request_user).exclude(seen=True).order_by("-date")
    return {"notifications": notifications}



