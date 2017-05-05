from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
# import mongoengine
# user = authenticate(username=username, password=password)
# assert isinstance(user, mongoengine.django.auth.User)
from pymongo.errors import DuplicateKeyError

from .models import Track, Artist


class HomePageView(generic.ListView):
    template_name = 'manage_music/index.html'
    context_object_name = 'top_alphabetical_track_list'

    def get_queryset(self):
        """Return the top five alphabetic tracks."""
        return Track.objects.order_by('-name')[:5]


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
            return render(request, 'manage_music/index.html', {
                'error_message': "Track already exists",
            })
        else:
            return HttpResponseRedirect(reverse('manage_music:index'))
