from django.shortcuts import render, get_list_or_404, get_object_or_404
#from django.template import RequestContext
from django.http import HttpResponseRedirect
from poll.models import Poll, Time, Option
from poll.forms import OptionForm, PollForm, TimeFormSet, TimeFormSetHelper
from django.views import generic
from django.views.generic.base import View
import hashlib
import time


class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'poll_list'
    error_template_name = 'poll/error.html'

    def get_queryset(self):
        return Poll.objects.filter(hidden=False).order_by('title')

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'poll/results.html'
    error_template_name = 'poll/error.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        poll = get_object_or_404(Poll, pk=pk)
        if  'admin_key' in self.kwargs:
            admin_key = self.kwargs['admin_key']
        else:
            admin_key = ""
        if poll.hidden and poll.admin_hash != admin_key:
            return render(request, self.error_template_name, {'message': "Admin Key doesn't matches"})
        else:
            options = poll.get_all_options()
            days = poll.get_days_times()
            votes = poll.get_participants_times()
            return render(request, self.template_name, {'poll': poll, 'options': options, 'days': days, "votes": votes})

class VoteView(View):
    form_class = OptionForm
    template_name = 'poll/vote.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        poll = get_object_or_404(Poll, pk=pk)
        form = self.form_class(pk)
        return render(request, self.template_name, {'form': form, "poll": poll})

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        poll = get_object_or_404(Poll, pk=self.kwargs['pk'])
        form = self.form_class(poll.id, request.POST)
        if form.is_valid() and self.constraints_met(poll, form):
            form.save(commit=True)
            return HttpResponseRedirect('/poll/' + str(poll.id))
        return render(request, self.template_name, {'form': form, "poll": poll})

    def constraints_met(self, poll, form):
        options = poll.get_all_options();
        votes = {}
        form = form.cleaned_data
        options_picked = 0;
        max_participants = poll.participants_option
        constraints_met = True

        # Check that only one time has been picked
        if poll.one_option and 'time_id' in form:
            options_picked = form['time_id'].count()
            constraints_met = constraints_met and (options_picked == 1)

        # Check if max number participants reached
        if max_participants > -1:
            for time in form['time_id']:
                current_particiapnts = Option.objects.filter(time_id=time.id).count()
                constraints_met = constraints_met and (current_particiapnts < max_participants)
        return constraints_met

class CreateView(generic.CreateView):
    form_class = PollForm
    model = Poll
    template_name = 'poll/create.html'
    success_url = '/poll/'

    def get(self, request, *args, **kwargs):
        '''
        Function to handle get requests and generate form and formset
        '''
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        '''
        Function that handles post requests. Tests if the poll and form times are
        valid.
        '''
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        '''
        Function that is called if a form is valid. Saves the poll and redirects to the
        success page.
        '''
        self.object = form.save(commit=False)
        # Generate hash for admin url using form data and current time, ugly but does the job
        hash = hashlib.sha256()
        form_string = str(form)
        current_time = str(time.time())
        hash.update(form_string + current_time)
        self.object.admin_hash = hash.hexdigest()
        self.object.save()
        response_url = self.get_success_url() + str(self.object.id) + "/addTime/" +  self.object.admin_hash
        return HttpResponseRedirect(response_url)

    def form_invalid(self, form):
        '''
        Function that is called if a form is invlaid. reloads the form page.
        '''
        context = self.get_context_data(form=form)
        return self.render_to_response(context, status=400)

class AddTimeView(generic.CreateView):
    form_class = TimeFormSet
    form_helper = TimeFormSetHelper
    model = Time
    template_name = 'poll/addTime.html'
    success_url = '/poll/'
    error_template_name = 'poll/error.html'

    def get(self, request, *args, **kwargs):
        '''
        Function to handle get requests and generate form and formset
        '''
        pk = self.kwargs['pk']
        admin_key = self.kwargs['admin_key']
        self.object = None
        poll = get_object_or_404(Poll, pk=pk)
        if poll.admin_hash == admin_key:
            formset = self.form_class()
            helper = self.form_helper()
            context = self.get_context_data(formset=formset, helper=helper)
            return self.render_to_response(context)
        else:
            return render(request, self.error_template_name, {'message': "Admin Key doesn't matches"})

    def post(self, request, *args, **kwargs):
        '''
        Function that handles post requests. Tests if the poll and form times are
        valid.
        '''
        pk = self.kwargs['pk']
        admin_key = self.kwargs['admin_key']
        self.object = None
        poll = get_object_or_404(Poll, pk=pk)
        if poll.admin_hash == admin_key:
            form = self.form_class(self.request.POST)
            if form.is_valid() and self.form_contains_time(form):
                return self.form_valid(form, poll)
            else:
                return self.form_invalid(form)
        else:
            return render(request, self.error_template_name, {'message': "Admin Key doesn't matches"})

    def form_valid(self, formset, poll):
        '''
        Function that is called if a form is valid. Saves the poll and redirects to the
        success page.
        '''
        for form in formset.cleaned_data:
            if 'time' in form:
                time = Time(time = form['time'])
                time.poll_id = poll
                self.object = time.save()
        response_url = self.success_url
        return HttpResponseRedirect(response_url)

    def form_invalid(self, form):
        '''
        Function that is called if a form is invlaid. reloads the form page.
        '''
        helper = self.form_helper()
        context = self.get_context_data(formset=form, helper=helper)
        return self.render_to_response(context, status=400)

    def form_contains_time(self, formset):
        for form in formset.cleaned_data:
            if 'time' in form:
                return True
        return False

class EditView(generic.UpdateView):
    model = Poll
    form_class = PollForm
    success_url = '/poll/'
    template_name = 'poll/create.html'
    error_template_name = 'poll/error.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        pk = self.kwargs['pk']
        admin_key = self.kwargs['admin_key']
        poll = get_object_or_404(Poll, pk=pk)
        if poll.admin_hash == admin_key:
            form = self.form_class(instance=poll, update=True, pk=poll.id, adminHash=admin_key)
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        else:
            return render(request, self.error_template_name, {'message': "Admin Key doesn't matches"})


    def post(self, request, *args, **kwargs):
        self.object = None
        pk = self.kwargs['pk']
        admin_key = self.kwargs['admin_key']
        poll = get_object_or_404(Poll, pk=pk)
        if poll.admin_hash == admin_key:
            form = self.form_class(self.request.POST, instance=poll)
            if form.is_valid():
                return self.form_valid(form, poll)
            else:
                return self.form_invalid(form)
        else:
            return render(request, self.error_template_name, {'message': "Admin Key doesn't matches"})

    def form_valid(self, form, poll):
        '''
        Function that is called if a form is valid. Saves the poll and redirects to the
        success page.
        '''
        self.object = form.save()
        response_url = self.get_success_url() + str(poll.id) + "/addTime/" +  poll.admin_hash
        return HttpResponseRedirect(response_url)

    def form_invalid(self, form):
        '''
        Function that is called if a form is invlaid. reloads the form page.
        '''
        context = self.get_context_data(form=form)
        return self.render_to_response(context, status=400)
