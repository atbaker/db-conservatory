# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Database'
        db.create_table(u'spinner_database', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ports', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=50)),
        ))
        db.send_create_signal(u'spinner', ['Database'])

        # Adding model 'Container'
        db.create_table(u'spinner_container', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('uri', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('database', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spinner.Database'])),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'spinner', ['Container'])


    def backwards(self, orm):
        # Deleting model 'Database'
        db.delete_table(u'spinner_database')

        # Deleting model 'Container'
        db.delete_table(u'spinner_container')


    models = {
        u'spinner.container': {
            'Meta': {'object_name': 'Container'},
            'container_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'database': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spinner.Database']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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