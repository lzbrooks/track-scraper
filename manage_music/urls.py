from django.conf.urls import url

from . import views

app_name = 'manage_music'
urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='index'),
    url(r'^about/$', views.AboutPageView.as_view(), name='about'),
    url(r'^tracks/add/$', views.MusicDatabaseView.as_view(), name='add_track'),
    url(r'^tracks/refresh/$', views.MusicDatabaseView.as_view(), name='refresh_tracks'),

]
