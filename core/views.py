#-*- coding:utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView

import flickrapi

from secret import passwords

import logging
logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.info('Before')


def require_flickr_auth(view):
    '''View decorator, redirects users to Flickr when no valid
    authentication token is available.
    '''

    def protected_view(request, *args, **kwargs):
        if 'token' in request.session:
            token = request.session['token']
            log.info('Getting token from session: %s' % token)
        else:
            token = None
            log.info('No token in session')

        f = flickrapi.FlickrAPI(passwords.FLICKR_API_KEY,passwords.FLICKR_API_SECRET,token=token,store_token=False)

        if token:
            # We have a token, but it might not be valid
            log.info('Verifying token')
            try:
                f.auth_checkToken()
            except flickrapi.FlickrError:
                token = None
                del request.session['token']

        if not token:
            # No valid token, so redirect to Flickr
            log.info('Redirecting user to Flickr to get frob')
            url = f.web_login_url(perms='read')
            return HttpResponseRedirect(url)

        # If the token is valid, we can call the decorated view.
        log.info('Token is valid')

        return view(request, *args, **kwargs)

    return protected_view

def callback(request):
    log.info('We got a callback from Flickr, store the token')

    f = flickrapi.FlickrAPI(passwords.FLICKR_API_KEY,passwords.FLICKR_API_SECRET, store_token=False)

    frob = request.GET['frob']
    token = f.get_token(frob)
    request.session['token'] = token

    return HttpResponseRedirect('/content')

@require_flickr_auth
def content(request):
    return HttpResponse('Welcome, oh authenticated user!')

# Create your views here.

class AngularApp(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(AngularApp, self).get_context_data(**kwargs)
        context['ANGULAR_URL'] = settings.ANGULAR_URL
        log.info('We got a callback from Flickr, store the token')
        return context


class SampleView(View):
    """View to render django template to angular"""
    def get(self, request):
        log.info('We got a callback from Flickr, store the token')
        return HttpResponse("OK!")


class NgTemplateView(View):
    """View to render django template to angular"""
    def get(self, request):
        log.info('We got a callback from Flickr, store the token')
        return render(request, 'template.html', {"django_variable": "This is django context variable"})
