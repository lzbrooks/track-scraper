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
            artist = save_artist(favourite_track)
            track = save_track(artist, favourite_track)
            save_recording(favourite_track, track)
            save_album(artist, favourite_track, track)
            # "name": "Toy",
            # "performer": "에프엑스(f(x))",
            # "year": 20130729,
            # 2013 07 29
            # "release_name": "Pink Tape (Vol. 2)",
    log.info("Finished Scraper Practice")


def get_request_json(user, index):
    webpage_url = "https://8tracks.com/users/" + str(user) + "/favorite_tracks" + \
                  "?page=" + str(index) + "&format=jsonh"
    request = get(webpage_url)
    request_json = request.json()
    return request_json


def save_artist(favourite_track):
    artist = Artist()
    artist.name = favourite_track["performer"]
    artist.save()
    return artist


def save_track(artist, favourite_track):
    track = Track()
    track.name = favourite_track["name"]
    track.artists = [artist]
    track.save()
    return track


def save_recording(favourite_track, track):
    recording = Recording()
    recording.tracks = [track]
    recording.web_page = favourite_track["url"]
    recording.save()


def save_album(artist, favourite_track, track):
    album = Album()
    album.name = favourite_track["release_name"]
    album.artists = [artist]
    album.tracks = [track]
    album.release_date = get_release_date(favourite_track["year"])
    album.save()


def get_release_date(integer_date):
    if len(str(integer_date)) == 4:
        return datetime.strptime(str(integer_date), "%Y")
    if len(str(integer_date)) == 6:
        return datetime.strptime(str(integer_date), "%Y%m")
    if len(str(integer_date)) == 8:
        return datetime.strptime(str(integer_date), "%Y%m%d")
