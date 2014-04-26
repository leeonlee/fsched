# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Department'
        db.create_table(u'schedulizer_department', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'schedulizer', ['Department'])

        # Adding model 'Attribute'
        db.create_table(u'schedulizer_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'schedulizer', ['Attribute'])

        # Adding model 'Course'
        db.create_table(u'schedulizer_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('crn', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedulizer.Department'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedulizer.Attribute'], null=True, blank=True)),
        ))
        db.send_create_signal(u'schedulizer', ['Course'])


    def backwards(self, orm):
        # Deleting model 'Department'
        db.delete_table(u'schedulizer_department')

        # Deleting model 'Attribute'
        db.delete_table(u'schedulizer_attribute')

        # Deleting model 'Course'
        db.delete_table(u'schedulizer_course')


    models = {
        u'schedulizer.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'schedulizer.course': {
            'Meta': {'object_name': 'Course'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedulizer.Attribute']", 'null': 'True', 'blank': 'True'}),
            'crn': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedulizer.Department']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        u'schedulizer.department': {
            'Meta': {'object_name': 'Department'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['schedulizer']