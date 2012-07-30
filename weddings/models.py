from django.db import models
# from django.db.models import signals
# from weddings.signals import invitation_created


class Invitation(models.Model):
    class Meta:
        verbose_name = "Invitation letter"
        verbose_name_plural = "Invitation letters"

    invite_code = models.CharField(
            help_text="leave it empty, it will be generated automatically on creation of invitation",
            verbose_name=u'invitation code',
            max_length=6)

    invitation_text = models.ForeignKey("InvitationTextTemplate",
                verbose_name=u'Invitation text template')

    friends = models.ManyToManyField("WeddingGuest", related_name="+", blank=True,
                verbose_name=u'Related friends for invitation')

    def __unicode__(self):
        return self.invite_code

# signals.pre_save.connect(invitation_created, sender=Invitation)


class InvitationTextTemplate(models.Model):
    class Meta:
        verbose_name = u'Invitation text template'
        verbose_name_plural = u'Invitation text templates'

    name = models.CharField(max_length=150, verbose_name=u'Name of template',
            help_text='Its used only for administrators to make sense out of template name')
    title = models.CharField(max_length=255, verbose_name=u'Title of invitation')
    body = models.TextField(verbose_name=u'Body of invitation')

    def __unicode__(self):
        return self.name


class WeddingGuest(models.Model):
    class Meta:
        verbose_name = u'Wedding guest'
        verbose_name_plural = u'Wedding guests'

    RSVP_ANSWERS = (
            (0, "Not answered"),
            (1, "Will attend"),
            (2, "Will not attend"),
            (3, "Maybe")
        )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    invitation = models.ForeignKey('Invitation', blank=True, null=True, on_delete=models.SET_NULL,
                            verbose_name=u'Invitation letter guest is assigned')

    # invited by others
    invited = models.BooleanField(default=False, verbose_name=u'Is he invited by other guest?')
    invited_by = models.ForeignKey('WeddingGuest', blank=True, null=True, verbose_name=u'Invited by who?')

    email = models.CharField(max_length=255, blank=True, null=True)

    rsvp_answer = models.PositiveSmallIntegerField(choices=RSVP_ANSWERS, default=0)
    rsvp_change_datetime = models.DateTimeField(blank=True, null=True, verbose_name=u'RSVP answered date time')

    def _get_fullname(self):
        return "%s %s" % (self.first_name, self.last_name)
    full_name = property(_get_fullname)

    def __unicode__(self):
        if self.email == "":
            return "%s %s" % (self.first_name, self.last_name)

        return "%s %s <%s>" % (self.first_name, self.last_name, self.email)


class CodeGuess(models.Model):
    class Meta:
        verbose_name = u'Invitation code guess'
        verbose_name_plural = u'Invitation code guesses'

    ip = models.IPAddressField(verbose_name=u'IP address')
    when_tried = models.DateTimeField(auto_now=True, auto_now_add=True, verbose_name=u'When')
    guess_code = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'Invitation code guessed')

    def __unicode__(self):
        return "%s - %s - %s" % (self.when_tried, self.ip, self.guess_code)
