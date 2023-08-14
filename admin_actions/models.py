from django.db import models
from project.utils import datetime_now


class AdminAction(models.Model):
    created_at = models.DateTimeField(default=datetime_now, editable=False)
    admin_fullname = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    action_text = models.TextField(default="", blank=True)
