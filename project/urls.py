"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from core.views import AngularApp, NgTemplateView, Login, authUser, registerUser, requestPhotos, Search, searchword, Photo

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registeruser/$', registerUser),
    url(r'^photos/(?P<photo_type>[\w]+)/$', Photo.as_view(), name='Photo'),
    url(r'^photos/$', Photo.as_view(),name='Photo'),
    url(r'^searchword/$', searchword),
    url(r'^search/$', Search.as_view(), name="Search"),
    url(r'^auth/$', authUser),
    url(r'^login/$', Login.as_view(), name="Login"),
] + static(settings.ANGULAR_URL, document_root=settings.ANGULAR_ROOT)
