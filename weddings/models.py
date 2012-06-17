from django.db import models


class Invitation(models.Model):
    invite_code = models.CharField(
            help_text="leave it empty, it will be generated automatically on creation of invitation",
            max_length=6)
    invitation_text = models.ForeignKey("InvitationTextTemplate")


class InvitationTextTemplate(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __unicode__(self):
        return self.name


class WeddingGuest(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    # invited by others
    invited = models.BooleanField(default=False)
    email = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s %s <%s>" % (self.first_name, self.last_name, self.email)
