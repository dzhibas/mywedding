from django.db import models
from datetime import datetime
from django.conf.global_settings import LANGUAGES
from django.utils.translation import ugettext as _
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

    questions = models.ForeignKey("Poll", verbose_name=u'Questions for invitation', blank=True, null=True)

    friends = models.ManyToManyField("WeddingGuest", related_name="+", blank=True,
                verbose_name=u'Related friends for invitation')

    invitation_language = models.CharField(max_length=7, choices=LANGUAGES, default='en')

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
            (0, _("Not answered")),
            (1, _("Will attend")),
            (2, _("Will not attend")),
            (3, _("Maybe"))
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


class QuestionManager(models.Manager):

    def create_poll(self, poll, question, choices):
        """ create a poll with available chices
            choices must be an iterable object
        """
        q = Question(poll=poll, question=question)
        q.save()
        for c in choices:
            Choice(text=c, question=q).save()
        return q


class Poll(models.Model):
    """ poll """

    title = models.TextField('Title')
    description = models.TextField('Poll description', blank=True)

    def __unicode__(self):
        return self.title

    def add_question(self, question, answers):
        Question.objects.create_poll(self, question, answers)


class Question(models.Model):
    """ Poll question """

    question = models.TextField('Question')
    poll = models.ForeignKey(Poll, related_name="questions")

    objects = QuestionManager()

    def user_choice(self, user):
        """ return user choice for this poll """
        try:
            return UserChoice.objects.get(user=user, choice__question=self).choice
        except UserChoice.DoesNotExist:
            pass
        return None

    def votes(self):
        """ return the vote number """
        return UserChoice.objects.filter(choice__question=self).count()

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    """ poll choice """

    question = models.ForeignKey(Question, related_name="choices")
    text = models.CharField('Answer', max_length=255)

    def __unicode__(self):
        return self.text

    def vote(self, user):
        """ user vote for this choice """
        if not self.question.user_choice(user):
            UserChoice(user=user, choice=self).save()
            return True
        return False

    def votes(self):
        return self.users.all().count()

    def percentage(self):
        total = self.question.votes()
        if total == 0:
            return 0
        return round((self.votes() * 100.0) / total, 1)


class UserChoice(models.Model):
    """
    it represents the vote for each user with timestamp
    """
    choice = models.ForeignKey(Choice, related_name="users")
    weddingguest = models.ForeignKey(WeddingGuest, related_name="poll_answers")
    invitation = models.ForeignKey(Invitation, related_name="poll_answers")
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ("choice", "invitation")
