# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'WeddingGuest.email'
        db.alter_column('weddings_weddingguest', 'email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'WeddingGuest.email'
        raise RuntimeError("Cannot reverse this migration. 'WeddingGuest.email' and its values cannot be restored.")

    models = {
        'weddings.codeguess': {
            'Meta': {'object_name': 'CodeGuess'},
            'guess_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'when_tried': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'weddings.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'+'", 'blank': 'True', 'to': "orm['weddings.WeddingGuest']"}),
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
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.Invitation']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invited_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.WeddingGuest']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'rsvp_answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'rsvp_change_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['weddings']