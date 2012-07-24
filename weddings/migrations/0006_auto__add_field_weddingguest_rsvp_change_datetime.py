# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WeddingGuest.rsvp_change_datetime'
        db.add_column('weddings_weddingguest', 'rsvp_change_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field friends on 'Invitation'
        db.create_table('weddings_invitation_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('invitation', models.ForeignKey(orm['weddings.invitation'], null=False)),
            ('weddingguest', models.ForeignKey(orm['weddings.weddingguest'], null=False))
        ))
        db.create_unique('weddings_invitation_friends', ['invitation_id', 'weddingguest_id'])


    def backwards(self, orm):
        # Deleting field 'WeddingGuest.rsvp_change_datetime'
        db.delete_column('weddings_weddingguest', 'rsvp_change_datetime')

        # Removing M2M table for field friends on 'Invitation'
        db.delete_table('weddings_invitation_friends')


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
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['weddings.WeddingGuest']"}),
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
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'rsvp_answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'rsvp_change_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['weddings']