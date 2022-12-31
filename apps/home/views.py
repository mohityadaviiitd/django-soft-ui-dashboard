# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.authentication.models import TwitterUser, Timeline, Video
from django.shortcuts import redirect
from .forms import ImageForm
import os

import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render


def search(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)
        

        results = r.json()['items']

        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }
    html_template = loader.get_template('home/search2.html')
    return HttpResponse(html_template.render(context, request))

def playlist(request):
    auth_user={}
    auth_user['screen_name']="unauth"
    auth_user['status']=False
    auth_user['staff']=False
    if request.user.is_staff:
        auth_user['staff']=True
    if (request.user.is_authenticated):
        auth_user_obj=TwitterUser.objects.get(user=request.user)
        auth_user['screen_name']=auth_user_obj.screen_name
        auth_user['status']=auth_user_obj.status


    videoData = Video.objects.filter(status=True).order_by('date_time')
    a=0
    videosArr=[]
    for data in videoData:
        videoObj={}
        if a==0:
            videoObj['top']=True
            a=1
        videoObj['video_id']=data.video_id
        videoObj['thumbnail']=data.thumbnail
        videoObj['title']=data.title
        videoObj['duration']=data.duration
        videoObj['screen_name']=data.screen_name
        videoObj['url']=data.url
        videosArr.append(videoObj)

    context = {'segment': 'index', 'videos':videosArr, 'auth_user':auth_user}
    html_template = loader.get_template('home/playlist.html')
    return HttpResponse(html_template.render(context, request))

def add_playlist(request):
    usr='Anonymous'
    if (request.user.is_authenticated):
        usr=request.user.username
    if request.method == 'POST':
        title = request.POST['title']
        thumbnail= request.POST['thumbnail']
        url= request.POST['url']
        duration= request.POST['duration']
        videoObj = Video(title=title, thumbnail=thumbnail, duration=duration, url=url, screen_name=usr)
        videoObj.status=True
        videoObj.save()
    return redirect("playlist")

@login_required(login_url="/login/")
def delete_playlist(request):

    if request.method == 'POST':
        thought = request.POST['deleteid']
        videoObj = Video.objects.get(video_id=thought)
        videoObj.status=False
        videoObj.save()
    return redirect("playlist")

@login_required(login_url="/login/")
def index(request):
    auth_user={}
    auth_user_obj=TwitterUser.objects.get(user=request.user)
    auth_user['twitter_id']=auth_user_obj.twitter_id
    auth_user['screen_name']=auth_user_obj.screen_name
    auth_user['name']=auth_user_obj.name
    auth_user['status']=auth_user_obj.status
    if auth_user_obj.image !='':
        auth_user['image']=True
    else:
        auth_user['image']=False
    userData = TwitterUser.objects.filter(status=True)
    usersArr=[]
    for data in userData:
        userObj={}
        userObj['twitter_id']=data.twitter_id
        userObj['screen_name']=data.screen_name
        userObj['name']=data.name
        if data.image !='':
            userObj['image']=True
        else:
            userObj['image']=False
        usersArr.append(userObj)
    auth_user['count']=len(usersArr)
    context = {'segment': 'index', 'users':usersArr, 'auth_user':auth_user}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def delete_thought(request):

    if request.method == 'POST':
        thought = request.POST['deleteid']
        timelineObj = Timeline.objects.get(timeline_id=thought)
        timelineObj.status=False
        timelineObj.save()
    return redirect("timeline")


@login_required(login_url="/login/")
def update_photo(request):
    old_image = TwitterUser.objects.get(screen_name=request.user.username)
    form = ImageForm(request.POST, request.FILES, instance=old_image)
    if form.is_valid():
        form.save()
        return redirect("profile/"+request.user.username)



@login_required(login_url="/login/")
def profile(request, screen_name=""):
    if screen_name=="me":
        screen_name=request.user.username
    req_user={}
    req_user_obj=TwitterUser.objects.get(screen_name=screen_name)
    req_user['staff']=False
    if req_user_obj.user.is_staff:
        req_user['staff']=True
    req_user['twitter_id']=req_user_obj.twitter_id
    req_user['screen_name']=req_user_obj.screen_name
    req_user['name']=req_user_obj.name
    req_user['status']=req_user_obj.status
    if req_user_obj.image !='':
        req_user['image']=True
    else:
        req_user['image']=False

    auth_user={}
    auth_user['staff']=False
    if request.user.is_staff:
        auth_user['staff']=True
    auth_user_obj=TwitterUser.objects.get(user=request.user)
    # auth_user['twitter_id']=auth_user_obj.twitter_id
    auth_user['screen_name']=request.user.username
    # auth_user['name']=auth_user_obj.name
    auth_user['status']=auth_user_obj.status
    if auth_user_obj.image !='':
        auth_user['image']=True
    else:
        auth_user['image']=False

    userData = TwitterUser.objects.filter(status=True)
    usersArr=[]
    for data in userData:
        userObj={}
        userObj['twitter_id']=data.twitter_id
        userObj['screen_name']=data.screen_name
        userObj['name']=data.name
        if data.image !='':
            userObj['image']=True
        else:
            userObj['image']=False
        usersArr.append(userObj)
    auth_user['count']=len(usersArr)


    timelineData=Timeline.objects.filter(status=True, user=req_user_obj.user).order_by('-date_time')
    timelineArrs=[]
    for data in timelineData:
        timelineArr={}
        usr=TwitterUser.objects.get(user=data.user)
        timelineArr['timeline_id']=data.timeline_id
        timelineArr['screen_name']=usr.screen_name
        timelineArr['name']=usr.name
        timelineArr['thought']=data.thought
        timelineArr['date_time']=str(data.date_time)
        if usr.image !='':
            timelineArr['image']=True
        else:
            timelineArr['image']=False
        timelineArrs.append(timelineArr)

    context = {'segment': 'index','req_user':req_user, 'users':usersArr, ' auth_user':auth_user, 'timeline': timelineArrs}
    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def post_thought(request):
    if request.method == 'POST':
        thought = request.POST['name']
        timelineObj = Timeline(user=request.user,
                                thought=thought,
                                status=True
                                )
        timelineObj.save()
    return redirect("timeline")

@login_required(login_url="/login/")
def timeline(request):

    timelineData=Timeline.objects.filter(status=True).order_by('-date_time')
    timelineArrs=[]
    for data in timelineData:
        timelineArr={}
        usr=TwitterUser.objects.get(user=data.user)
        timelineArr['timeline_id']=data.timeline_id
        timelineArr['screen_name']=usr.screen_name
        timelineArr['name']=usr.name
        timelineArr['thought']=data.thought
        timelineArr['date_time']=str(data.date_time)
        if usr.image !='':
            timelineArr['image']=True
        else:
            timelineArr['image']=False
        timelineArrs.append(timelineArr)
        
    auth_user={}
    auth_user['staff']=False
    if request.user.is_staff:
        auth_user['staff']=True
    auth_user_obj=TwitterUser.objects.get(user=request.user)
    # auth_user['twitter_id']=auth_user_obj.twitter_id
    auth_user['screen_name']=request.user.username
    # auth_user['name']=auth_user_obj.name
    auth_user['status']=auth_user_obj.status
    # if auth_user_obj.image !='':
    #     auth_user['image']=True
    # else:
    #     auth_user['image']=False
    # userData = TwitterUser.objects.filter(status=True)
    # usersArr=[]
    # for data in userData:
    #     userObj={}
    #     userObj['twitter_id']=data.twitter_id
    #     userObj['screen_name']=data.screen_name
    #     userObj['name']=data.name
    #     if data.image !='':
    #         userObj['image']=True
    #     else:
    #         userObj['image']=False
    #     usersArr.append(userObj)
    # auth_user['count']=len(usersArr)
    context = {'segment': 'index', 'timeline':timelineArrs, 'auth_user':auth_user}
    html_template = loader.get_template('home/api-view.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
