from django.contrib import admin
from poll.models import Poll, Time, Option

class ChoiceInline(admin.TabularInline):
    model = Time
    extra = 3

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Option)