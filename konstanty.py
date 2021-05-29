PREFIX = 'prefix'
SUFFIX = 'suffix'
NOT_FOUND = 'nenalezeno'

from enum import Enum

class Odezva(Enum):
    CLOSE = -1
    TEXT = 1
    METHOD = 2
    TEXT_BY_USER = 3
    REACTION = 4

class ResponseType(Enum):
    CLOSE = -1
    NOTHING = 0
    MESSAGE = 1
    ANSWER = 2
    REACTION = 3

class Reaction:
    WAVE = "👋"
    THUMB_UP = "👍"
    CRY = "😭"
    EYES = "👀"