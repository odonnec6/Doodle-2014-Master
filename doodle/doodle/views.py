from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.base import View
from django.shortcuts import render_to_response


def home(request):
    context = RequestContext(request)

    return render_to_response('base/home.html', context)
