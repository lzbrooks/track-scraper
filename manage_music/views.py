from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
# import mongoengine
#
# user = authenticate(username=username, password=password)
# assert isinstance(user, mongoengine.django.auth.User)
from pymongo.errors import DuplicateKeyError

from .track_scraper import scraper_practice
from .models import Track, Artist


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        top_alphabetical_track_list = Track.objects.order_by('-name')[:5]
        context = {'top_alphabetical_track_list': top_alphabetical_track_list}
        return render(request, 'manage_music/index.html', context)


class AboutPageView(TemplateView):
    template_name = "about.html"


class MusicDatabaseView(TemplateView):
    def post(self, request):
        try:
            artist = Artist()
            artist.name = request.POST['track_artist']
            track = Track()
            track.name = request.POST['track_name']
            track.artists = [artist]
        except (KeyError, DuplicateKeyError):
            # Redisplay the question voting form.
            return render(request, 'polls/index.html', {
                'error_message': "Track already exists",
            })
        else:
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:index'))

    def get(self, request, **kwargs):
        scraper_practice()



