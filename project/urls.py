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
from core.views import AngularApp, NgTemplateView, Search, Photos, Login, authUser, registerUser

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/$', authUser),
    url(r'^registeruser/$', registerUser),
    url(r'^login/$', Login.as_view(), name="Login"),
    url(r'^search/', Search.as_view(), name="Search"),
    url(r'^photos/', Photos.as_view(), name="Photos"),
] + static(settings.ANGULAR_URL, document_root=settings.ANGULAR_ROOT)
