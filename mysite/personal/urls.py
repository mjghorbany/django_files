from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^search', views.search, name='search'),
    #url(r'^search',views.search, name='search'),
]

