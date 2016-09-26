# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Poll'
        db.create_table(u'poll_poll', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('creator', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('creator_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('one_option', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('participants_option', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal(u'poll', ['Poll'])

        # Adding model 'Time'
        db.create_table(u'poll_time', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Poll'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'poll', ['Time'])

        # Adding model 'Option'
        db.create_table(u'poll_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Time'])),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'poll', ['Option'])


    def backwards(self, orm):
        # Deleting model 'Poll'
        db.delete_table(u'poll_poll')

        # Deleting model 'Time'
        db.delete_table(u'poll_time')

        # Deleting model 'Option'
        db.delete_table(u'poll_option')


    models = {
        u'poll.option': {
            'Meta': {'object_name': 'Option'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Time']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
        },
        u'poll.time': {
            'Meta': {'object_name': 'Time'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['poll.Poll']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['poll']