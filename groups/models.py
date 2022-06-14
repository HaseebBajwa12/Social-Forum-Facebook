from django.db import models

# Create your models here.

from user_management.models import User


class Group(models.Model):
    user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE, null=True, blank=True)
    user2 = models.ForeignKey(User, related_name="second_person", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    group_type = models.BooleanField(default=False)