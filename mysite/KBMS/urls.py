from django.conf.urls import url
from . import views

app_name='KBMS'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^ontology', views.ontology, name='ontology'),
    url(r'^curation', views.curation, name='curation'),
    url(r'^cy2neo', views.cy2neo, name='cy2neo'),
    url(r'^rule_engine', views.rule_engine, name='rule_engine'),
    url(r'^node/add', views.NodeCreate.as_view(), name='node_add'),

    url(r'^upload_csv', views.upload_csv, name='upload_csv'),
    # /KBMS/node/<pk>/
    #url(r'^node/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /KBMS/node/<pk>/favorite/
    url(r'^node/(?P<pk>[0-9]+)/favorite/$', views.favorite, name='favorite'),

    #url(r'^node/(?P<node_id>[0-9]+)/$', views.detail, name='detail_db'),


    #From Music app
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login_user/$', views.login_user, name='login_user'),
    #url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    #url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_ontology/$', views.create_ontology, name='create_ontology'),
    # url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    # url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    # url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    # url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
]