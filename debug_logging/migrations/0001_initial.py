# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DebugLogRecord'
        db.create_table('debug_logging_debuglogrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('project_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('request_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('settings_pickled', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timer_utime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('timer_stime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('timer_cputime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('timer_total', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('timer_vcsw', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('timer_ivcsw', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sql_num_queries', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sql_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sql_queries_pickled', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cache_num_calls', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cache_time', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cache_hits', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cache_misses', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cache_sets', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cache_gets', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cache_get_many', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cache_deletes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cache_calls_pickled', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('debug_logging', ['DebugLogRecord'])


    def backwards(self, orm):
        
        # Deleting model 'DebugLogRecord'
        db.delete_table('debug_logging_debuglogrecord')


    models = {
        'debug_logging.debuglogrecord': {
            'Meta': {'object_name': 'DebugLogRecord'},
            'cache_calls_pickled': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cache_deletes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cache_get_many': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cache_gets': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cache_hits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cache_misses': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cache_num_calls': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cache_sets': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cache_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'request_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'settings_pickled': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sql_num_queries': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sql_queries_pickled': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sql_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timer_cputime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timer_ivcsw': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timer_stime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timer_total': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timer_utime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'timer_vcsw': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['debug_logging']
