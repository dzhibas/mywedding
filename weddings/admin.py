from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from models import Invitation, InvitationTextTemplate, WeddingGuest, CodeGuess

admin.site.register(Invitation)
admin.site.register(InvitationTextTemplate, MarkdownModelAdmin)
admin.site.register(WeddingGuest)
admin.site.register(CodeGuess)
