# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import login_view, register_user, index, twitter_callback, twitter_login, twitter_logout
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/jwt/', view=obtain_auth_token),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('social_login/', include('allauth.urls')),


    path('ind/', index, name='index'),
    path('twitter_login', twitter_login, name='twitter_login'),
    path('twitter_callback', twitter_callback, name='twitter_callback'),
    path('twitter_logout', twitter_logout, name='twitter_logout'),

]
