#-*- coding:utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from core.models import Photo

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

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
