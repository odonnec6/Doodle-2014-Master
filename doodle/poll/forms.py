from django import forms
from poll.models import Poll, Time, Option
from django.forms.models import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, HTML

choices = ( (1,'Yes'),
            (0,'No'),
          )

class PollForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder':"Name of Poll"}),
        label='Name of the Poll'
    )

    creator = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder':"Email"}),
        label='Email'
    )

    creator_name = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder':"Your Name"}),
        label='Your Name'
    )

    location = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder':"Location"}),
        label='Location'
    )

    description = forms.CharField(
        max_length=128,
        widget=forms.TextInput(attrs={'placeholder':"Description"}),
        label='Description'
    )

    hidden = forms.TypedChoiceField(
        choices=choices,
        widget=forms.RadioSelect, coerce=int,
        label='Do you want this poll to be private?'
    )

    one_option = forms.TypedChoiceField(
        choices=choices,
        widget=forms.RadioSelect,
        coerce=int,
        label='Can participants only choose one option?'
    )

    participants_option = forms.IntegerField(
        label='Max number of participants per option. Not required.',
        required=False
    )

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('update'):
            update = kwargs.pop('update')
            adminHash = kwargs.pop('adminHash')
            pk = kwargs.pop('pk')
        else:
            update = False
        super(PollForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'poll_form'
        self.helper.form_method = 'post'
        if update:
            self.helper.form_action = '/poll/' + str(pk) + '/edit/' + adminHash + '/'
        else:
            self.helper.form_action = '/poll/create/'

        self.helper.add_input(Submit('submit', 'Submit'))

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Poll
        exclude = ('admin_hash',)

    def clean(self):
        cleaned_input = self.cleaned_data
        participants = cleaned_input.get('participants_option')
        if not(participants > 0):
            participants = -1
            cleaned_input['participants_option'] = participants
        return cleaned_input

class TimeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TimeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'poll_form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


    class Meta:
        # Provide an association between the ModelForm and a model
        exclude = ('poll_id',)
        model = Time

class OptionForm(forms.ModelForm):
    time_id = forms.ModelMultipleChoiceField(
        queryset=Time.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple
    )
    user = forms.CharField()
    anonymous = forms.TypedChoiceField(
        choices=choices,
        widget=forms.RadioSelect,
        coerce=int,
        help_text="Do you wish to be anonymous?"
    )

    def __init__(self, fk, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        # Filter the options based on the foreign key
        self.fields['time_id'].queryset = Time.objects.filter(poll_id=fk)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Option

TimeFormSet = formset_factory(TimeForm, can_delete=True, extra=5)

class TimeFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TimeFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True,
        self.layout = Layout(
            Field('time', id="time-field", css_class="timefields")
        )
        self.add_input(Submit("submit", "Save"))
