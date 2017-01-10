#-*- coding:utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from core.models import Photo
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

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

class Search(View):
    """View to render django template to angular"""
    def get(self, request):
        text = Photo.queryListByKeyword('child')
        log.info(text)
        return HttpResponse(text)

class Photos(View):
    """docstring for Photos"""
    def get(self, request):
        text = Photo.queryListByType('popular')
        return HttpResponse(text)

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
