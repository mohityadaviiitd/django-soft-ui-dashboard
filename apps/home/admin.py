# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from apps.models import Book
admin.site.register(Book)

# from apps.home.models import user_info

from apps.authentication.models import TwitterAuthToken, TwitterUser, Timeline, Video

admin.site.register(TwitterAuthToken)
admin.site.register(TwitterUser)
admin.site.register(Timeline)
admin.site.register(Video)
# admin.site.register(user_info)
# Register your models here.
