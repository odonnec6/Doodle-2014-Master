from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from users import views

urlpatterns = patterns('',
        url(r'^$', login_required(views.ProfileView.as_view()), name='users'),
        url(r'^create/$', views.CreateView.as_view(), name='create'),
        url(r'^login/$', 'django.contrib.auth.views.login'),
        url(r'^logout/$', 'django.contrib.auth.views.logout'),
        )