from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.cache import never_cache
from weddings.models import WeddingGuest, Invitation


class RsvpAnswerView(RedirectView):
    url = reverse_lazy("invitation")
    query_string = True
    permanent = True

    @never_cache
    def get(self, request, *args, **kwargs):
        response = super(RsvpAnswerView, self).get(request, *args, **kwargs)

        # if unkown actor
        if 'pin_provided' not in request.session or 'logged_pin' not in request.session:
            return response

        # double check if invitation exists
        invitation = self.check_pin(request.session['logged_pin'])
        if invitation == False:
            return response

        answer_id = kwargs['answer_id']

        # check if provided answer id is valid,if not redirect
        possible_answers = [a[0] for a in list(WeddingGuest.RSVP_ANSWERS)]
        if answer_id not in possible_answers:
            return response

        # check if logged in user can answer for person provided
        person_id = kwargs['person_id']

        return response

    def check_pin(self, pin):
        try:
            return Invitation.objects.get(invite_code=pin)
        except Invitation.DoesNotExist:
            return False
