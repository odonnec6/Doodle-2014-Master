# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table(u'comment_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Poll'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('creator_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'comment', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table(u'comment_comment')


    models = {
        u'comment.comment': {
            'Meta': {'object_name': 'Comment'},
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Poll']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'poll.poll': {
            'Meta': {'object_name': 'Poll'},
            'creator': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'one_option': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participants_option': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['comment']