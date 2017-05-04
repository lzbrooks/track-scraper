from background_task import background
from mongoengine import NotUniqueError
from pymongo.errors import DuplicateKeyError
from requests import get
import logging
from datetime import datetime

from manage_music.models import Track, Artist, Recording, Album


log = logging.getLogger(__name__)


@background(schedule=60)
def refresh_favourite_tracks():
    # log.info("Starting Scraper Practice")
    print("Starting Scraper Practice")
    request_json = get_favourite_track_request_json("dakre", 1)
    favorite_tracks_pagination = request_json["pagination"]
    total_pages = favorite_tracks_pagination["total_pages"]
    for index in range(1, total_pages):
        request_json = get_favourite_track_request_json("dakre", index)
        all_favorite_tracks = request_json["favorite_tracks"]
        for favourite_track in all_favorite_tracks:
            # TODO: there's a way to grab the artist info when playing tracks
            # todo: investigate for aliases, description, homepage
            # https://8tracks.com/sets/197579681/next?player=sm&include=track%5Bfaved%2Bannotation%2Bartist_details%5D&mix_id=2183081&track_id=17451458&format=jsonh
            # info is legit pulled from like wikipedia (sidebar and first paragraph)
            artist = save_artist(favourite_track)
            track = save_track(artist, favourite_track)
            recording = save_recording(artist, favourite_track, track)
            album = save_album(favourite_track, track)
            if album is not None:
                print('Track: {track} by {artist} in {album} of {year}'.format(
                   track=track.name, artist=artist.name, album=album.name, year=album.release_date))
            else:
                print('Track: {track} by {artist}'.format(
                    track=track.name, artist=artist.name))
    # log.info("Finished Scraper Practice")
    print("Finished Scraper Practice")


def get_favourite_track_request_json(user, index):
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
        for artist_object in Artist.objects(name=artist.name):
            artist = artist_object
    return artist


def save_track(artist, favourite_track):
    track = Track()
    track.name = favourite_track["name"]
    track.artists = [artist]
    try:
        track.save()
    except (DuplicateKeyError, NotUniqueError):
        for track_object in Track.objects(name=track.name):
            track = track_object
    return track


def save_recording(artist, favourite_track, track):
    recording = Recording()
    recording.name = track.name
    recording.tracks = [track]
    recording.artists = [artist]
    recording.web_page = favourite_track["url"]
    try:
        recording.save()
    except (DuplicateKeyError, NotUniqueError):
        # todo: maybe try to get this proper from the database
        return recording
    return recording


def save_album(favourite_track, track):
    if favourite_track["release_name"] is not None:
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
    if integer_date is None:
        return
    if len(str(integer_date)) == 4:
        return datetime.strptime(str(integer_date), "%Y")
    if len(str(integer_date)) == 6:
        return datetime.strptime(str(integer_date), "%Y%m")
    if len(str(integer_date)) == 8:
        return datetime.strptime(str(integer_date), "%Y%m%d")
