# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Container.id'
        db.delete_column(u'spinner_container', u'id')


        # Changing field 'Container.container_id'
        db.alter_column(u'spinner_container', 'container_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, primary_key=True))
        # Adding unique constraint on 'Container', fields ['container_id']
        db.create_unique(u'spinner_container', ['container_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Container', fields ['container_id']
        db.delete_unique(u'spinner_container', ['container_id'])


        # User chose to not deal with backwards NULL issues for 'Container.id'
        raise RuntimeError("Cannot reverse this migration. 'Container.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Container.id'
        db.add_column(u'spinner_container', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # Changing field 'Container.container_id'
        db.alter_column(u'spinner_container', 'container_id', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        u'spinner.container': {
            'Meta': {'object_name': 'Container'},
            'container_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'database': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spinner.Database']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'spinner.database': {
            'Meta': {'object_name': 'Database'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ports': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['spinner']