# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('timeline', views.timeline, name='timeline'),
    path('delete_thought', views.delete_thought, name='delete_thought'),
    path('post_thought', views.post_thought, name='post_thought'),
    path('search', views.search, name='search'),
    path('playlist', views.playlist, name='playlist'),
    path('add_playlist', views.add_playlist, name='add_playlist'),
    path('delete_playlist', views.delete_playlist, name='delete_playlist'),
    path('profile/<str:screen_name>', views.profile, name='profile'),
    path('update_photo', views.update_photo, name='update_photo'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
