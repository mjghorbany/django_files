from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^ontology', views.ontology, name='ontology'),
    url(r'^node/add', views.NodeCreate.as_view(), name='node_add'),

    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    url(r'^node/(?P<node_id>[0-9]+)/$', views.detail, name='detail_db'),

    #url(r'^search', views.search, name='search'),
    #url(r'^search',views.search, name='search'),
]