from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from weddings.models import *
from forms import InvitationForm


class InvitationAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends', )
    fields = ('invite_code', 'invitation_text', 'invitation_language', 'questions', 'invitation_guests', 'friends',)
    list_display = ('invite_code', 'who_invited', 'invitation_text__name', 'invitation_language', 'invitation_text__title', 'questions')
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


class CodeGuessAdmin(admin.ModelAdmin):
    list_display = ('ip', 'when_tried', 'guess_code', )
    date_hierarchy = 'when_tried'
    search_fields = ['ip']

admin.site.register(CodeGuess, CodeGuessAdmin)


class GuestsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'invitation_letter', 'rsvp_answer_display', 'rsvp_change_datetime')
    list_filter = ('rsvp_answer', )
    search_fields = ['email', 'first_name', 'last_name']
    fields = (('first_name', 'last_name'), 'email', 'invitation',
        ('invited', 'invited_by'),
        ('rsvp_answer', 'rsvp_change_datetime'))

    def invitation_letter(self, obj):
        if obj.invitation == None:
            return "<div style='background-color:#FB7474;color:#fff;width:100%%;height:100%%'>Not assigned</div>"
        return obj.invitation
    invitation_letter.allow_tags = True

    def rsvp_answer_display(self, obj):
        COLORS = ['#FFC63E', '#008F06', '#CC0000', '#B45353']
        return "<div style='background-color:%s;color:#fff;width:100%%;height:100%%'>%s</div>" % (COLORS[obj.rsvp_answer], obj.get_rsvp_answer_display())
    rsvp_answer_display.allow_tags = True

admin.site.register(WeddingGuest, GuestsAdmin)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 4


class PollAlladmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAlladmin)
