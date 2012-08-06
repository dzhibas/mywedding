# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Poll'
        db.create_table('weddings_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('weddings', ['Poll'])

        # Adding model 'Question'
        db.create_table('weddings_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['weddings.Poll'])),
        ))
        db.send_create_signal('weddings', ['Question'])

        # Adding model 'Choice'
        db.create_table('weddings_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['weddings.Question'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('weddings', ['Choice'])

        # Adding model 'UserChoice'
        db.create_table('weddings_userchoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='users', to=orm['weddings.Choice'])),
            ('weddingguest', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poll_answers', to=orm['weddings.WeddingGuest'])),
            ('invitation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poll_answers', to=orm['weddings.Invitation'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('weddings', ['UserChoice'])

        # Adding unique constraint on 'UserChoice', fields ['choice', 'invitation']
        db.create_unique('weddings_userchoice', ['choice_id', 'invitation_id'])

        # Adding field 'Invitation.questions'
        db.add_column('weddings_invitation', 'questions',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weddings.Poll'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'UserChoice', fields ['choice', 'invitation']
        db.delete_unique('weddings_userchoice', ['choice_id', 'invitation_id'])

        # Deleting model 'Poll'
        db.delete_table('weddings_poll')

        # Deleting model 'Question'
        db.delete_table('weddings_question')

        # Deleting model 'Choice'
        db.delete_table('weddings_choice')

        # Deleting model 'UserChoice'
        db.delete_table('weddings_userchoice')

        # Deleting field 'Invitation.questions'
        db.delete_column('weddings_invitation', 'questions_id')


    models = {
        'weddings.choice': {
            'Meta': {'object_name': 'Choice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': "orm['weddings.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'questions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.Poll']", 'null': 'True', 'blank': 'True'})
        },
        'weddings.invitationtexttemplate': {
            'Meta': {'object_name': 'InvitationTextTemplate'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'weddings.poll': {
            'Meta': {'object_name': 'Poll'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'weddings.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['weddings.Poll']"}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'weddings.userchoice': {
            'Meta': {'unique_together': "(('choice', 'invitation'),)", 'object_name': 'UserChoice'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'to': "orm['weddings.Choice']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poll_answers'", 'to': "orm['weddings.Invitation']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'weddingguest': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poll_answers'", 'to': "orm['weddings.WeddingGuest']"})
        },
        'weddings.weddingguest': {
            'Meta': {'object_name': 'WeddingGuest'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invitation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.Invitation']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'invited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'invited_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weddings.WeddingGuest']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'rsvp_answer': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'rsvp_change_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['weddings']