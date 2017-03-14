from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Authors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField(blank=True, null=True)
    birth_date =  models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    oauth_id = models.IntegerField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True,default=0)
    photo = models.URLField(blank=True,null=True,default=0)

    total_comments = models.IntegerField(blank=True, null=True,default=0)
    logged_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'authors'