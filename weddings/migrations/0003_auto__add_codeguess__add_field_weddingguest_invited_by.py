# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CodeGuess'
        db.create_table('weddings_codeguess', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('when', self.gf('django.db.models.fields.TimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('guess_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('weddings', ['CodeGuess'])

        # Adding field 'WeddingGuest.invited_by'
        db.add_column('weddings_weddingguest', 'invited_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weddings.WeddingGuest'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'CodeGuess'
        db.delete_table('weddings_codeguess')

        # Deleting field 'WeddingGuest.invited_by'
        db.delete_column('weddings_weddingguest', 'invited_by_id')


    models = {
        'weddings.codeguess': {
            'Meta': {'object_name': 'CodeGuess'},
            'guess_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'when': ('django.db.models.fields.TimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'weddings.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation_text': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.InvitationTextTemplate']"}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'weddings.invitationtexttemplate': {
            'Meta': {'object_name': 'InvitationTextTemplate'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'weddings.weddingguest': {
            'Meta': {'object_name': 'WeddingGuest'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.Invitation']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invited_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.WeddingGuest']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['weddings']