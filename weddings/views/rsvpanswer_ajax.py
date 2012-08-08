from weddings.models import WeddingGuest, Invitation
import datetime
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.utils.translation import activate


def answer(request, *args, **kwargs):
    response_data = {}
    response_data['success'] = 'false'

    json_data = simplejson.dumps(response_data)
    response = HttpResponse(json_data, mimetype='application/javascript')

    # if unkown actor
    if 'pin_provided' not in request.session or 'logged_pin' not in request.session:
        return response

    # double check if invitation exists
    invitation = check_pin(request.session['logged_pin'])
    if invitation == False:
        return response

    answer_id = int(kwargs['answer_id'])

    # check if provided answer id is valid,if not redirect
    possible_answers = [a[0] for a in list(WeddingGuest.RSVP_ANSWERS)]
    if answer_id not in possible_answers:
        return response

    # check if logged in user can answer for person provided
    person_id = int(kwargs['person_id'])
    persons_ids_allowed = [person.id for person in invitation.weddingguest_set.all()]

    if person_id not in persons_ids_allowed:
        return response

    try:
        selected_person = invitation.weddingguest_set.get(id=person_id)
        if selected_person.rsvp_answer != answer_id:
            selected_person.rsvp_answer = answer_id
            selected_person.rsvp_change_datetime = datetime.datetime.today()
            selected_person.save()
    except WeddingGuest.DoesNotExist:
        return response

    activate(invitation.invitation_language)

    response_data = {}
    response_data['success'] = 'true'
    response_data['new_status'] = _(selected_person.get_rsvp_answer_display())

    json_data = simplejson.dumps(response_data)
    response = HttpResponse(json_data, mimetype='application/json')

    return response


def check_pin(pin):
    try:
        return Invitation.objects.get(invite_code__iexact=pin)
    except Invitation.DoesNotExist:
        return False
