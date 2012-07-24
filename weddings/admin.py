from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from models import Invitation, InvitationTextTemplate, WeddingGuest, CodeGuess
from forms import InvitationForm


class InvitationAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends', )
    fields = ('invite_code', 'invitation_text', 'invitation_guests', 'friends',)
    list_display = ('invite_code', 'who_invited', 'invitation_text__name', 'invitation_text__title')
    form = InvitationForm

    def who_invited(self, obj):
        who = ""
        for guest in obj.weddingguest_set.all():
            who += str(guest) + ","
        return who

    def invitation_text__name(self, obj):
        return obj.invitation_text.name

    def invitation_text__title(self, obj):
        return obj.invitation_text.title

admin.site.register(Invitation, InvitationAdmin)
admin.site.register(InvitationTextTemplate, MarkdownModelAdmin)
admin.site.register(CodeGuess)


class GuestsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'rsvp_answer', 'rsvp_change_datetime')
    list_filter = ('rsvp_answer', )
    search_fields = ['email', 'first_name', 'last_name']

admin.site.register(WeddingGuest, GuestsAdmin)
