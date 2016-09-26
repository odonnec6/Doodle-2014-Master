# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Poll.time_created'
        db.add_column(u'poll_poll', 'time_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 4, 2, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Poll.time_created'
        db.delete_column(u'poll_poll', 'time_created')


    models = {
        u'poll.option': {
            'Meta': {'object_name': 'Option'},
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_id': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['poll.Time']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'poll.poll': {
            'Meta': {'object_name': 'Poll'},
            'admin_hash': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'creator': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'one_option': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'participants_option': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'poll.time': {
            'Meta': {'object_name': 'Time'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Poll']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['poll']