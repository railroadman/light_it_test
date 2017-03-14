from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from soc_auth.models import Authors


class Messages(models.Model):
    message = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Authors)
    status = models.IntegerField(blank=True, null=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def time_ago(self):

        time_difference = timezone.now() - self.created_at
        return {"minutes": time_difference.total_seconds() / 60, "hours": time_difference.total_seconds() / 60 / 60,
                "days": time_difference.total_seconds() / 60 / 60 / 24}

    class Meta:
        db_table = 'messages'


class Comments(models.Model):
    message = models.ForeignKey('Messages', on_delete=models.CASCADE,related_name="comments",related_query_name="comment")
    comment_txt = models.TextField(blank=True, null=True)
    author = models.ForeignKey(Authors)
    status = models.IntegerField(blank=True, null=True, default=1)
    parent_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def time_ago(self):
        time_difference = timezone.now() - self.created_at
        return {"minutes": time_difference.total_seconds() / 60, "hours": time_difference.total_seconds() / 60 / 60,
                "days": time_difference.total_seconds() / 60 / 60 / 24}

    class Meta:
        db_table = 'comments'
