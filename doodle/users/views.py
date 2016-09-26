from django.shortcuts import get_list_or_404
from django.views import generic
from django.contrib.auth.models import User
from users.forms import UserForm
from poll.models import Poll
from django.http import HttpResponseRedirect


# Create your views here.

class ProfileView(generic.TemplateView):
    model = User
    template_name = 'users/profile.html'


    def get(self, request, *args, **kwargs):
        self.object = None
        current_user = request.user
        polls = Poll.objects.filter(creator=current_user.email)
        context = self.get_context_data(polls=polls)
        return self.render_to_response(context)

class CreateView(generic.CreateView):
    form_class = UserForm
    model = User
    template_name = 'users/create.html'
    success_url = '/users/'

    def get(self, request, *args, **kwargs):
        self.object = None
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.success_url)
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = form_class(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        '''
        Function that is called if a form is valid. Saves the poll and redirects to the
        success page.
        '''
        user = form.save()
        # Hash password
        user.set_password(user.password)
        user.save()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        '''
        Function that is called if a form is invlaid. reloads the form page.
        '''
        context = self.get_context_data(form=form)
        return self.render_to_response(context, status=400)
