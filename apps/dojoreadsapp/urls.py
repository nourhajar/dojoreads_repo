from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.readall),
    url(r'^books/add$', views.add),
    url(r'^books/(?P<id>\d+)$', views.readone),
    url(r'^users/(?P<id>\d+)$', views.readuser),
    url(r'^books/(?P<id>\d+)/add_review', views.addreview),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^create_book$', views.create_book),
]