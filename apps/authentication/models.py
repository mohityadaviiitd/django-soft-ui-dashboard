# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.conf import settings 
import uuid, random, datetime

class TwitterAuthToken(models.Model):
    oauth_token = models.CharField(default=uuid.uuid4, max_length=255)
    oauth_token_secret = models.CharField(default=uuid.uuid4, max_length=255)

    def __str__(self):
        return self.oauth_token

def get_profile_photo(self, filename):
    return f'apps/static/assets/img/profile_images/{self.pk}/{"profile_photo.png"}'


class TwitterUser(models.Model):
    twitter_id = models.CharField(default=uuid.uuid4, max_length=255)
    screen_name = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255)
    profile_image_url = models.CharField(max_length=255, null=True)
    twitter_oauth_token = models.ForeignKey(TwitterAuthToken, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True,  upload_to=get_profile_photo)
    status=models.BooleanField(default=False)

    def get_profile_photo(self):
        return str(self.image)[str(self.image).index(f'apps/static/assets/img/profile_images/{self.pk}/'):]


    def __str__(self):
        return self.screen_name

class Timeline(models.Model):
    timeline_id=models.CharField(default=uuid.uuid4, primary_key=True, max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    thought = models.CharField(max_length=200)
    date_time=models.DateTimeField(default=datetime.datetime.now)
    status=models.BooleanField(default=False)

class Video(models.Model):
    video_id=models.CharField(default=uuid.uuid4, primary_key=True, max_length=255)
    thumbnail = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    date_time=models.DateTimeField(default=datetime.datetime.now)
    duration = models.CharField(max_length=200)
    status=models.BooleanField(default=True)
    screen_name=  models.CharField(default= "Anonymous", max_length=200)
    url=models.CharField(max_length=500)

# Create your models here.
