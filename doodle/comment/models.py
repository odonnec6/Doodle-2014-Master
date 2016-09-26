from django.db import models
from poll.models import Poll

class Comment(models.Model):
    poll_id = models.ForeignKey(Poll)
    title = models.CharField(max_length=128)
    creator_name = models.CharField(max_length=128, null=True)
    text = models.CharField(max_length=512, null=True)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        return self.title
