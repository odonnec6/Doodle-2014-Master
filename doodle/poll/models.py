from django.db import models
from datetime import datetime,date
from collections import OrderedDict

class Poll(models.Model):
    title = models.CharField(max_length=128)
    creator = models.EmailField(max_length=254)
    creator_name = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=128, null=True)
    hidden = models.BooleanField(default=False)
    one_option = models.BooleanField(default=False)
    participants_option = models.IntegerField(default=-1)
    admin_hash = models.CharField(max_length=64)
    time_created = models.DateTimeField(auto_now=True)

    def get_all_options(self):
        times = Time.objects.filter(poll_id=self.id)
        returnOptions = {}
        for time in times:
            options = Option.objects.filter(time_id=time.id)
            returnOptions[time] = options
        return returnOptions

    def get_days_times(self):
        '''
        Function that generates a dictionary of days and the times that can be
        voted on during that particular day,
        '''
        day_string = "%B %d, %Y"
        time_string = "%H:%M"
        times = Time.objects.filter(poll_id=self.id).order_by('time')
        returnOptions = OrderedDict()
        for time in times:
            date = time.time
            day = datetime.strftime(date, day_string)
            time = datetime.strftime(date, time_string)
            if day in returnOptions.keys():
                returnOptions[day].append(time)
            else:
                returnOptions[day] = [time]
        return returnOptions

    def get_participants_times(self):
        '''
        Generates a dictionary of people participating in a poll and their vote
        status for each of polls times.

        '''
        times = Time.objects.filter(poll_id=self.id)
        returnChoices = {}
        participantChoices = {} # Dictionary of participants and the times they voted for

        # Get all of the votes for the poll
        for time in times:
            choices = Option.objects.filter(time_id=time.id)
            # Iterate through votes and add to dictionary of partipants
            for choice in choices:
                if choice in participantChoices.keys():
                    participantChoices[choice].append(time.id)
                else:
                    participantChoices[choice] = []
                    participantChoices[choice].append(time.id)

        # Iterates through dictionary of participants and compares with all times
        # If they voted for a time, a true is added otherwise a false is added
        for participant in participantChoices:
            returnChoices[participant] = []
            for time in times:
                if time.id in participantChoices[participant]:
                    returnChoices[participant].append(True)
                else:
                    returnChoices[participant].append(False)
        return returnChoices

    def __unicode__(self):
        return self.title

class Time(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        ordering = ['-time']
        return self.time

class Option(models.Model):
    time_id = models.ManyToManyField(Time)
    user = models.CharField(max_length=128)
    anonymous = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user
