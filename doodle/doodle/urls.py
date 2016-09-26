from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'doodle.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^poll/', include('poll.urls', namespace="poll")),
    url(r'^users/', include('users.urls', namespace="users")),
)
