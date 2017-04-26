# from django.db import models
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, URLField


# Artist
class Artist(Document):
    name = StringField(required=True, unique=True)
    aliases = ListField(StringField())
    description = StringField()
    homepage = URLField()


# Genre
class Genre(Document):
    name = StringField(required=True, unique=True)
    description = StringField()


# Association
class Association(Document):
    name = StringField(required=True, unique=True)
    description = StringField()


# Track
class Track(Document):
    name = StringField(required=True, unique_with='artists')
    artists = ListField(ReferenceField(Artist))


class Recording(Document):
    tracks = ListField(ReferenceField(Track))
    artists = ListField(ReferenceField(Artist))
    version = StringField(unique_with=['tracks', 'artists'])
    description = StringField()
    play_time = StringField()
    lyrics = StringField()
    language = StringField()
    youtube_link = URLField()
    web_page = URLField()
    genres = ListField(ReferenceField(Genre))
    associations = ListField(ReferenceField(Association))


# MusicCollection
class MusicCollection(Document):
    name = StringField(required=True, unique_with='artists')
    artists = ListField(ReferenceField(Artist))
    description = StringField()
    picture_link = StringField()
    tracks = ListField(ReferenceField(Track))
    genres = ListField(ReferenceField(Genre))
    associations = ListField(ReferenceField(Association))

    meta = {'allow_inheritance': True}


class Album(MusicCollection):
    release_date = DateTimeField()


class Mix(MusicCollection):
    web_page = URLField()
