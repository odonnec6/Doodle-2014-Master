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
       # help_text="Please enter the name of the poll."
    )

    creator = forms.EmailField(
        max_length=254,
      #  help_text="Please enter a valid email address."
    )

    creator_name = forms.CharField(
        max_length=128,
    #    help_text="Please enter your name."
    )

    location = forms.CharField(
        max_length=128,
    #    help_text="Please enter the location of the meeting."
    )

    description = forms.CharField(
        max_length=128,
    #    help_text="Please enter the description of the meeting."
    )

    hidden = forms.TypedChoiceField(
        choices=choices,
        widget=forms.RadioSelect, coerce=int,
     #   help_text="Is the poll private?"
    )

    one_option = forms.TypedChoiceField(
        choices=choices,
        widget=forms.RadioSelect,
        coerce=int,
    #    help_text="Can only one option be chosen?"
    )

    participants_option = forms.IntegerField(
    #    help_text="Max number participants per option?"
    )

    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'poll_form'
        self.helper.form_method = 'post'
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
        if participants == 0:
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

TimeFormSet = formset_factory(TimeForm, can_delete=False, extra=5)

class TimeFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TimeFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.render_required_fields = True,
        self.add_input(Submit("submit", "Save"))
