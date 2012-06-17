# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invitation'
        db.create_table('weddings_invitation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invite_code', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('invitation_text', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weddings.InvitationTextTemplate'])),
        ))
        db.send_create_signal('weddings', ['Invitation'])

        # Adding model 'InvitationTextTemplate'
        db.create_table('weddings_invitationtexttemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('weddings', ['InvitationTextTemplate'])

        # Adding model 'WeddingGuest'
        db.create_table('weddings_weddingguest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('invited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('weddings', ['WeddingGuest'])


    def backwards(self, orm):
        # Deleting model 'Invitation'
        db.delete_table('weddings_invitation')

        # Deleting model 'InvitationTextTemplate'
        db.delete_table('weddings_invitationtexttemplate')

        # Deleting model 'WeddingGuest'
        db.delete_table('weddings_weddingguest')


    models = {
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
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['weddings']