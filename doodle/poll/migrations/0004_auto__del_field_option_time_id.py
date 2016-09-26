# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Option.time_id'
        db.delete_column(u'poll_option', 'time_id_id')

        # Adding M2M table for field time_id on 'Option'
        m2m_table_name = db.shorten_name(u'poll_option_time_id')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('option', models.ForeignKey(orm[u'poll.option'], null=False)),
            ('time', models.ForeignKey(orm[u'poll.time'], null=False))
        ))
        db.create_unique(m2m_table_name, ['option_id', 'time_id'])


    def backwards(self, orm):
        # Adding field 'Option.time_id'
        db.add_column(u'poll_option', 'time_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['poll.Time']),
                      keep_default=False)

        # Removing M2M table for field time_id on 'Option'
        db.delete_table(db.shorten_name(u'poll_option_time_id'))


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