# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
import uuid, random


# class user_info(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     twitter_room = models.CharField(default='0', max_length=100, null=False, blank=True) # 0 : not part, # 1: is part #2: requested
#     games_room = models.CharField(default='0', max_length=100, null=False, blank=True)
#     developer_room = models.CharField(default='0', max_length=100, null=False, blank=True)
#     artificial_intelligence_room = models.CharField(default='0', max_length=100, null=False, blank=True)
#     status = models.CharField(default='0',max_length=90) # if part of any room it is 1
#     profile_photo = models.CharField(default='0', max_length=100, null=False, blank=True)

# Create your models here.

