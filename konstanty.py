PREFIX = 'prefix'
SUFFIX = 'suffix'
NOT_FOUND = 'nenalezeno'

TYPE_RUTINNE_CLOSE = -1
TYPE_RUTINNE_TEXT = 1
TYPE_RUTINNE_METHOD = 2
TYPE_RUTINNE_TEXT_BY_USER = 3

from enum import Enum

class ResponseType(Enum):
    CLOSE = -1
    NOTHING = 0
    MESSAGE = 1
    ANSWER = 2
    REACTION = 3

class Reaction(Enum):
    WAVE = "👋"
    THUMB_UP = "👍"
    CRY = "😭"
    EYES = "👀"