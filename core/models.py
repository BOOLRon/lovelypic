from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from enum import Enum, unique
from secret import passwords
import urllib.request

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Photodb(models.Model):
    photo_from = models.CharField(max_length=20, blank=True)
    take_by_userid = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=30, blank=True)
    image_url = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=100, blank=True)
    aspect = models.FloatField()
    photoext = models.OneToOneField('Photoext', on_delete=models.CASCADE, blank=True)
    category = models.CharField(max_length=20, blank=True)

    @classmethod
    def createByJSONObj(JSONObj,category):
        url = JSONObj['url']
        if url:
            newPhoto = Photodb(link=url)
            newPhoto.photo_from = '500px'
            newPhoto.name = JSONObj['name']
            newPhoto.image_url = JSONObj['image_url']
            width = float(JSONObj['width'])
            height = float(JSONObj['height'])
            newPhoto.photoext = Photoext.createByJSONObj(JSONObj)
            if width > 0 and height > 0:
                newPhoto.aspect = width/height
            newPhoto.category = category
            return newPhoto
        return None

class Photoext(models.Model):
    camera = models.CharField(max_length=100, blank=True)
    lens = models.CharField(max_length=100, blank=True)
    focal_length = models.CharField(max_length=10, blank=True)
    iso = models.CharField(max_length=10, blank=True)
    shutter_speed = models.CharField(max_length=10, blank=True)
    aperture = models.CharField(max_length=10, blank=True)
    latitude = models.FloatField()
    location = models.FloatField()
    taken_at = models.CharField(max_length=100, blank=True)
    width = models.FloatField()
    height = models.FloatField()

    @classmethod
    def createByJSONObj(JSONObj):
        photoExtObj = Photoext()
        photoExtObj.camera = JSONObj['camera']
        photoExtObj.lens = JSONObj['lens']
        photoExtObj.focal_length = JSONObj['focal_length']
        photoExtObj.iso = JSONObj['iso']
        photoExtObj.shutter_speed = JSONObj['shutter_speed']
        photoExtObj.aperture = JSONObj['aperture']
        photoExtObj.latitude = float(JSONObj['latitude'])
        photoExtObj.location = float(JSONObj['location'])
        photoExtObj.taken_at = JSONObj['taken_at']
        photoExtObj.width = float(JSONObj['width'])
        photoExtObj.height = float(JSONObj['height'])
        return photoExtObj



class Photofavorite(models.Model):
    photoid = models.ForeignKey('Photodb', on_delete=models.CASCADE)
    userid = models.ForeignKey('auth.User', on_delete=models.CASCADE)


@unique
class PhotoFeature(Enum):
    POPULAR = 'popular'
    HIGHEST_RATED = 'highest_rated'
    UPCOMING = 'upcoming'
    EDITORS = 'editors'
    FRESH_TODAY = 'fresh_today'
    FRESH_YESTERDAY = 'fresh_yesterday'
    FRESH_WEEK = 'fresh_week'

@unique
class PhotoCategory(Enum):
    UNCATEGORIZED = 'Uncategorized'
    ABSTRACT = 'Abstract'
    ANIMALS = 'Animals'
    BLACK_AND_WHITE = 'Black and White'
    CELEBRITIES = 'Celebrities'
    CITY_AND_ARCHITECTURE = 'City and Architecture'
    COMMERCIAL = 'Commercial'
    CONCERT = 'Concert'
    FAMILY = 'Family'
    FASHION = 'Fashion'
    FILM = 'Film'
    FINE_ART = 'Fine Art'
    FOOD = 'Food'
    JOURNALISM = 'Journalism'
    LANDSCAPES = 'Landscapes'
    MACRO = 'Macro'
    NATURE = 'Nature'
    NUDE = 'Nude'
    PEOPLE = 'People'
    PERFORMING_ARTS = 'Performing Arts'
    SPORT = 'Sport'
    STILL_LIFE = 'Still Life'
    STREET = 'Street'
    TRANSPORTATION = 'Transportation'
    TRAVEL = 'Travel'
    UNDERWATER = 'Underwater'
    URBAN_EXPLORATION = 'Urban Exploration'
    WEDDING = 'Wedding'

PHOTO_BASE_URL = 'https://api.500px.com/v1/photos?consumer_key=' + passwords.ConsumerKey
LIST_SORTVALUE = 'created_at'
LIST_IMAGE_SIZE = '3'
LIST_INCLUDE_STORE = '1'
LIST_INCLUDE_STATES = '1'


import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


"""Photo object from 500px"""
class Photo(object):
    """docstring for Photo"""
    def __init__(self, arg):
        super(Photo, self).__init__()
        self.arg = arg

    def queryListByType(photoFeature):
        url = PHOTO_BASE_URL
        url += '&sort={0}&image_size={1}&include_store={2}&include_states={3}&feature={4}'.format(LIST_SORTVALUE,LIST_IMAGE_SIZE,LIST_INCLUDE_STORE,LIST_INCLUDE_STATES,photoFeature)
        response = urllib.request.urlopen(url)
        data = response.read()
        responseText = data.decode('utf-8')
        return responseText

    def queryListByKeyword(searchWord):
        url = PHOTO_BASE_URL
        url += '&sort={0}&image_size={1}&term={2}'.format(LIST_SORTVALUE,LIST_IMAGE_SIZE,searchWord)
        log.info(url)
        response = urllib.request.urlopen(url)
        data = response.read()
        responseText = data.decode('utf-8')
        return responseText





