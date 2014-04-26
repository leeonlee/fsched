# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Course.desc'
        db.add_column(u'schedulizer_course', 'desc',
                      self.gf('django.db.models.fields.CharField')(default='a', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Course.desc'
        db.delete_column(u'schedulizer_course', 'desc')


    models = {
        u'schedulizer.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'schedulizer.course': {
            'Meta': {'object_name': 'Course'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['schedulizer.Attribute']", 'null': 'True', 'blank': 'True'}),
            'credits': ('django.db.models.fields.IntegerField', [], {}),
            'crn': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'days': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schedulizer.Department']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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