from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError
from requests import get
import logging
from datetime import datetime

from manage_music.models import Track, Artist, Recording, Album


log = logging.getLogger(__name__)


def scraper_practice():
    log.info("Starting Scraper Practice")
    request_json = get_request_json("dakre", 1)
    favorite_tracks_pagination = request_json["pagination"]
    total_pages = favorite_tracks_pagination["total_pages"]
    for index in range(1, total_pages):
        request_json = get_request_json("dakre", index)
        all_favorite_tracks = request_json["favorite_tracks"]
        for favourite_track in all_favorite_tracks:
            # TODO: there's a way to grab the artist info when playing tracks
            # todo: investigate for aliases, description, homepage
            # https://8tracks.com/sets/197579681/next?player=sm&include=track%5Bfaved%2Bannotation%2Bartist_details%5D&mix_id=2183081&track_id=17451458&format=jsonh
            artist = save_artist(favourite_track)
            track = save_track(artist, favourite_track)
            save_recording(artist, favourite_track, track)
            save_album(favourite_track, track)
    log.info("Finished Scraper Practice")


def get_request_json(user, index):
    web_page_url = "https://8tracks.com/users/" + str(user) + "/favorite_tracks" + \
                  "?page=" + str(index) + "&format=jsonh"
    request = get(web_page_url)
    request_json = request.json()
    return request_json


def save_artist(favourite_track):
    artist = Artist()
    artist.name = favourite_track["performer"]
    # todo: append artist name as alias if different from name found
    try:
        artist.save()
    except (DuplicateKeyError, NotUniqueError):
        artist = Artist.objects(name=artist.name)
    return artist


def save_track(artist, favourite_track):
    artists = [artist]
    track = Track()
    track.name = favourite_track["name"]
    track.artists = artists
    try:
        track.save()
    except (DuplicateKeyError, NotUniqueError):
        track = Track.objects(name=track.name)
    return track


def save_recording(artist, favourite_track, track):
    artists = [artist]
    recording = Recording()
    recording.tracks = [track]
    recording.artists = artists
    recording.web_page = favourite_track["url"]
    try:
        recording.save()
    except (DuplicateKeyError, NotUniqueError):
        # todo: maybe try to get this proper from the database
        return recording
    return recording


def save_album(favourite_track, track):
    album = Album()
    album.name = favourite_track["release_name"]
    album.artists = track.artists
    album.tracks = [track]
    album.release_date = get_release_date(favourite_track["year"])
    try:
        album.save()
    except (DuplicateKeyError, NotUniqueError):
        # todo: maybe try to get this proper from the database
        return album
    return album


def get_release_date(integer_date):
    if len(str(integer_date)) == 4:
        return datetime.strptime(str(integer_date), "%Y")
    if len(str(integer_date)) == 6:
        return datetime.strptime(str(integer_date), "%Y%m")
    if len(str(integer_date)) == 8:
        return datetime.strptime(str(integer_date), "%Y%m%d")
