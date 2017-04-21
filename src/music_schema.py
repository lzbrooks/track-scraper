from mongoengine import *

connect('track_scraper')


class Artist(Document):
    name = StringField(required=True)
    aliases = ListField(StringField())
    description = StringField()
    homepage = StringField()


class Collection(Document):
    name = StringField(required=True)
    artists = ListField(ReferenceField(Artist))
    description = StringField()
    picture_link = StringField()
    tracks = ListField(ReferenceField(Track))
    genres = ListField(ReferenceField(Genre))
    associations = ListField(ReferenceField(Association))

    meta = {'allow_inheritance': True}


class Album(Collection):
    release_date = DateTimeField()


class Mix(Collection):
    web_page = StringField()


class Track(Document):
    name = StringField(required=True)
    artists = ListField(ReferenceField(Artist))
    description = StringField()
    play_time = StringField()
    lyrics = StringField()
    language = StringField()
    youtube_link = StringField()
    web_page = StringField()
    genres = ListField(ReferenceField(Genre))
    associations = ListField(ReferenceField(Association))

    meta = {'allow_inheritance': True}


class Remix(Track):
    original_tracks = ListField(ReferenceField(Track))


class Genre(Document):
    name = StringField(required=True)
    description = StringField()


class Association(Document):
    name = StringField(required=True)
    description = StringField()
