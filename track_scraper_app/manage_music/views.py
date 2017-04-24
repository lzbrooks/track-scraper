from django.shortcuts import render
from django.views.generic import TemplateView
# import mongoengine
#
# user = authenticate(username=username, password=password)
# assert isinstance(user, mongoengine.django.auth.User)
from .models import Track


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        top_alphabetical_track_list = Track.objects.order_by('-name')[:5]
        context = {'top_alphabetical_track_list': top_alphabetical_track_list}
        return render(request, 'manage_music/index.html', context)


class AboutPageView(TemplateView):
    template_name = "about.html"


# class MusicDatabaseView(TemplateView):
#     def get(self, request, **kwargs):
#
