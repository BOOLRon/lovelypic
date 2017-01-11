#-*- coding:utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from core.models import Photodb
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import datetime
import time
import json
import urllib

from core.config import PhotoFeature, PhotoCategory, PHOTO_BASE_URL, LIST_SORTVALUE, LIST_IMAGE_SIZE, LIST_INCLUDE_STORE, LIST_INCLUDE_STATES, TARGET_LOAD_TYPE, TARGET_LOAD_LIMIT_TIME

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

#[url : timestamp]
requestTimes = {}

def authUser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        return HttpResponse('login success')
    else:
        return HttpResponse('login fail')

@csrf_exempt
def registerUser(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    count_of_user = len(User.objects.filter(username=username))
    if count_of_user > 0:
        return HttpResponse('Account has been register')
    else:
        newUser = User.objects.create_user(username, email, password)
        newUser.save()
        return render(request, 'login_register.html')

def requestPhotos(request):
    # photoFeature = request.POST['photoFeature']
    # searchWord = request.POST['search']
    photoFeature = 'popular'
    if photoFeature:
        return requestThenStorePhotosByType(photoFeature)
    else:
        return requestThenStorePhotosBySearch(searchWord)

def requestThenStorePhotosByType(photoFeature):
    url = photoFeatureURL(photoFeature)
    if shouldRequestURL(photoFeature):
        # need to requeset then store
        requestThenStoreByURL(url,photoFeature)
    return requestDatabaseByType(photoFeature)

def requestThenStorePhotosBySearch(searchWord):
    url = photoSearchURL(searchWord)
    if shouldRequestURL(searchWord):
        # need to requeset then store
        requestThenStoreByURL(url,searchWord)
    return requestDatabaseBySearch(searchWord)

def requestThenStoreByURL(url,keyword):
    jsonDatas = json.loads(JSONStringFromURL(url))
    photos = jsonDatas['photos']
    for photo in photos:
        findPhotoSet = Photodb.objects.filter(link=photo['url'])
        if len(findPhotoSet) == 0:
            newPhoto = Photodb.createByJSONObj(photo,keyword)
            newPhoto.save()

def requestDatabaseByType(photoFeature):
    photoSet = Photodb.objects.filter(category=photoFeature)
    return HttpResponse(photoSet)

def requestDatabaseBySearch(searchWord):
    photoSet = Photodb.objects.filter(category=searchWord)
    return HttpResponse(photoSet)

def shouldRequestURL(keyword):
    now = time.time()
    if keyword in requestTimes:
        requestTime = requestTimes[keyword];
        if now - requestTime > TARGET_LOAD_LIMIT_TIME:
            return True
            return False
    else:
        requestTimes[keyword] = now
        return True

def photoFeatureURL(photoFeature):
    url = PHOTO_BASE_URL
    url += '&sort={0}&image_size={1}&include_store={2}&include_states={3}&feature={4}'.format(LIST_SORTVALUE,LIST_IMAGE_SIZE,LIST_INCLUDE_STORE,LIST_INCLUDE_STATES,photoFeature)
    return url

def photoSearchURL(searchWord):
    url = PHOTO_BASE_URL
    url += '&sort={0}&image_size={1}&term={2}'.format(LIST_SORTVALUE,LIST_IMAGE_SIZE,searchWord)
    return url

def JSONStringFromURL(url):
    log.info(url)
    response = urllib.request.urlopen(url)
    data = response.read()
    responseText = data.decode('utf-8')
    return responseText

class Login(View):
    def get(self, request):
        return render(request, 'login_register.html')

class AngularApp(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(AngularApp, self).get_context_data(**kwargs)
        context['ANGULAR_URL'] = settings.ANGULAR_URL
        log.info(context)
        log.info('from AngularApp')
        return context

# class SampleView(TemplateView):
#     """View to render django template to angular"""
#     def get(self, request):
#         text = 'It works'
#         return HttpResponse(text)

class NgTemplateView(View):
    """View to render django template to angular"""
    def get(self, request):
        log.info('from NgTemplateView')
        return render(request, 'template.html', {"django_variable": "This is django context variable"})
