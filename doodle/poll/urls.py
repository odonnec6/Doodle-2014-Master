from django.conf.urls import patterns, url
from poll import views

urlpatterns = patterns('',
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<pk>\d+)/$', views.ResultsView.as_view(), name='detail'),
        url(r'^(?P<pk>\d+)/vote/$', views.VoteView.as_view(), name='vote'),
        url(r'^(?P<pk>\d+)/edit/(?P<admin_key>.+)/$', views.EditView.as_view(), name='edit'),
        url(r'^(?P<pk>\d+)/addTime/(?P<admin_key>.+)/$', views.AddTimeView.as_view(), name='add_time'),
        url(r'^(?P<pk>\d+)/(?P<admin_key>.+)/$', views.ResultsView.as_view(), name='detail'),
        url(r'^create/$', views.CreateView.as_view(), name='create')
        )
