#-*- coding:utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from core.models import Photodb, Photofavorite
from django.contrib.auth import authenticate, login, logout
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
        login(request,user)
        return redirect('/photos/')
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
        login(request,newUser)
        return redirect('/photos/')


def requestPhotos(context):
    if 'photoFeature' in context:
        return requestThenStorePhotosByType(context['photoFeature'])
    else:
        if 'search' in context:
            return requestThenStorePhotosBySearch(context['search'])
        else:
            return requestThenStorePhotosByType('popular')

def requestFavoritePhotos(request):
    if request.user.is_authenticated:
        userid = request.user.id
        if userid != None:
            photoFavorites = Photofavorite.objects.filter(userid=userid)
            allFavoritePhotos = []
            for photoFavorite in photoFavorites:
                photoSet = Photodb.objects.filter(id=photoFavorite.photoid)
                if len(photoSet) > 0:
                    allFavoritePhotos.append(photoSet[0])
            if len(allFavoritePhotos)>0:
                return allFavoritePhotos
    return []

def favoriteAction(request):
    photo_id = request.GET.get('photo_id')
    log.info('hey')
    log.info(photo_id)
    if request.user.is_authenticated:
        return HttpResponse('TODO save into DB')
    else:
        return HttpResponse('not login')

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
            if newPhoto:
                newPhoto.save()

def requestDatabaseByType(photoFeature):
    photoSet = Photodb.objects.filter(category=photoFeature)
    return photoSet

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
    response = urllib.request.urlopen(url)
    data = response.read()
    responseText = data.decode('utf-8')
    return responseText

def searchword(request):
    searchword = request.POST['searchword']
    if searchword:
        return requestThenStorePhotosBySearch(searchword)
    else:
        HttpResponse('search faile')

def logoutRequest(request):
    logout(request)
    return redirect('/photos/')

class Photo(View):
    def get(self, request, photo_type = None):
        if photo_type == None:
            photo_type = 'popular'

        if photo_type == 'fav':
            photos = requestFavoritePhotos(request)
        else:
            photos = requestPhotos({'photoFeature' : photo_type})

        context = {'photo_type' : photo_type}
        if request.user.is_authenticated:
            context['authuser'] = request.user
        if len(photos)>0:
            context['photos'] = photos
        return render(request, 'html5up/index.html', context)

class Search(View):
    def get(self, request):
        return render(request, 'search.html')

class AngularApp(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(AngularApp, self).get_context_data(**kwargs)
        context['ANGULAR_URL'] = settings.ANGULAR_URL
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
