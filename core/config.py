
from enum import Enum, unique
from secret import passwords

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
LIST_IMAGE_SIZE = '4'
LIST_INCLUDE_STORE = '1'
LIST_INCLUDE_STATES = '1'

TARGET_LOAD_TYPE = (PhotoFeature.POPULAR, PhotoFeature.HIGHEST_RATED, PhotoFeature.UPCOMING, PhotoFeature.EDITORS, PhotoFeature.FRESH_TODAY)

# second
TARGET_LOAD_LIMIT_TIME = 7200


