# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Course.attribute'
        db.delete_column(u'schedulizer_course', 'attribute_id')

        # Adding M2M table for field attributes on 'Course'
        m2m_table_name = db.shorten_name(u'schedulizer_course_attributes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'schedulizer.course'], null=False)),
            ('attribute', models.ForeignKey(orm[u'schedulizer.attribute'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'attribute_id'])


    def backwards(self, orm):
        # Adding field 'Course.attribute'
        db.add_column(u'schedulizer_course', 'attribute',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedulizer.Attribute'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field attributes on 'Course'
        db.delete_table(db.shorten_name(u'schedulizer_course_attributes'))


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