from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from weddings.models import Invitation, UserChoice, WeddingGuest
from django.utils.html import escape


class InvitationView(TemplateView):
    template_name = "invitation.html"

    pin = None
    guest = None
    invitation = None

    def get(self, request, *args, **kwargs):
        # check if everything in place
        if 'pin_provided' not in request.session or 'logged_pin' not in request.session:
            return HttpResponseRedirect(reverse('pin1'))

        self.pin = request.session['logged_pin']

        invitation = self.check_pin(request.session['logged_pin'])

        if invitation == False:
            return HttpResponseRedirect(reverse('pin1'))

        self.invitation = invitation

        if 'logged_in_guest' in request.session:
            logged_guest_id = int(request.session['logged_in_guest'])
            try:
                self.guest = WeddingGuest.objects.get(pk=logged_guest_id)
            except:
                pass

        response = super(InvitationView, self).get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super(InvitationView, self).get_context_data(**kwargs)
        context['invitation'] = self.invitation
        context['guests'] = self.invitation.weddingguest_set.all()
        context['guest_count'] = len(context['guests'])

        answers = UserChoice.objects.filter(invitation=self.invitation)
        if self.guest != None:
            answers.filter(weddingguest=self.guest)

        all_choices = [answer.choice.pk for answer in answers]

        context['poll_answers'] = all_choices

        context['questions_has_answers'] = [answer.choice.question.pk for answer in answers]

        ff_answer = {}
        for answer in answers:
            if answer.freetext_answer != None and answer.freetext_answer != '':
                ff_answer[answer.choice.question.pk] = escape(answer.freetext_answer)

        context['ff_answers'] = ff_answer

        return context

    def check_pin(self, pin):
        try:
            return Invitation.objects.get(invite_code=pin)
        except Invitation.DoesNotExist:
            return False
