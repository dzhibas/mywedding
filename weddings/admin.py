# coding=utf-8

from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from weddings.models import *
from forms import InvitationForm
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.utils.translation import ugettext as _
from django.utils.translation import activate
from datetime import datetime

temp_answer_translations = (
            (0, _("Not answered")),
            (1, _("Will attend")),
            (2, _("Will not attend")),
            (3, _("Maybe"))
        )


def send_invitation(modeladmin, request, queryset):
    messages_to_send = []

    for invitation in queryset:
        emails = []
        guests = invitation.weddingguest_set.all()

        # activating invitation language
        activate(invitation.invitation_language)

        # lazy translating
        subject = _(u"Jūs pakviesti! Kur? Žiūrėkite į laiško vidų.")
        body_message = _(u"Jūsų kodas: %(code)s \nJo prireiks apsilankius svetainėje: http://rsvp.gang.lt")

        for g in guests:
            if g.email != None and g.email.strip() != '':
                emails.append(str(g.email))

        if len(emails) > 0:
            messages.info(request, "Successfully sent emails to: %s" % ','.join(emails))
            messages_to_send.append((subject, body_message % {'code': invitation.invite_code},
                'nikolajus@gmail.com',
                ['nikolajus@gmail.com', 'nikolajus@gmail.com']))

            invitation.email_sent = True
            invitation.email_sent_at = datetime.now()
            invitation.save()

        else:
            messages.error(request, "Invitation %s has no emails assigned" % invitation)

    if len(messages_to_send) > 0:
        send_mass_mail(messages_to_send, fail_silently=False)


send_invitation.short_description = "Send invitation to available recipients"


class InvitationAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends', )
    fields = ('invite_code', 'invitation_text', 'invitation_language', 'questions', 'invitation_guests', 'friends',)
    list_display = ('invite_code', 'who_invited', 'invitation_text__name', 'invitation_language', 'invitation_text__title', 'questions', 'email_sent', 'email_sent_at')
    form = InvitationForm
    actions = [send_invitation]

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


class UserChoiceAdmin(admin.ModelAdmin):
    model = UserChoice
    list_display = ('weddingguest', 'choice__question', 'choice', 'invitation', 'who_invited', )

    def choice__question(self, obj):
        return obj.choice.question

    def who_invited(self, obj):
        who = ""
        for guest in obj.invitation.weddingguest_set.all():
            who += str(guest) + ","
        return who

admin.site.register(UserChoice, UserChoiceAdmin)
