from django.shortcuts import render
from django.views.generic import TemplateView
# import mongoengine
#
# user = authenticate(username=username, password=password)
# assert isinstance(user, mongoengine.django.auth.User)


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class AboutPageView(TemplateView):
    template_name = "about.html"
