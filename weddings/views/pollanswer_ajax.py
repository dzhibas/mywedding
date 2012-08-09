from weddings.models import Invitation, Choice, UserChoice
from django.http import HttpResponse
from django.utils import simplejson


def poll_answer(request, *args, **kwargs):
    response_data = {}
    response_data['success'] = 'false'

    json_data = simplejson.dumps(response_data)
    response = HttpResponse(json_data, mimetype='application/javascript')

    if 'choice_id' not in kwargs:
        return response

    # if unkown actor
    if 'pin_provided' not in request.session or 'logged_pin' not in request.session:
        return response

    # double check if invitation exists
    invitation = check_pin(request.session['logged_pin'])
    if invitation == False:
        return response

    real_guests = invitation.weddingguest_set.filter(invited=False)
    real_guest_count = len(real_guests)
    wedding_guest = None

    if real_guest_count < 2:
        wedding_guest = real_guests[0]
    else:
        if 'logged_in_guest' in request.session:
            try:
                wedding_guest = invitation.wedding_guest.get(pk=int(request.session['logged_in_guest']))
            except:
                return response

    if wedding_guest == None:
        return response

    choice_id = int(kwargs['choice_id'])

    try:
        choice = Choice.objects.get(pk=choice_id)
    except:
        return response

    # check if he can answer this choice
    if invitation.questions != choice.question.poll:
        return response

    # check if there is no answer already for this question
    already_answed = UserChoice.objects.filter(choice__question=choice.question, invitation=invitation, weddingguest=wedding_guest)
    if len(already_answed) > 0:
        uc = already_answed[0]

        # if same answer dont do anything
        if uc.choice == choice:
            return response

        uc.choice = choice
        uc.save()
    else:
        try:
            uc = UserChoice()
            uc.choice = choice
            uc.weddingguest = wedding_guest
            uc.invitation = invitation
            uc.save()
        except:
            return response

    response_data = {}
    response_data['success'] = 'true'

    json_data = simplejson.dumps(response_data)
    response = HttpResponse(json_data, mimetype='application/json')

    return response


def check_pin(pin):
    try:
        return Invitation.objects.get(invite_code__iexact=pin)
    except Invitation.DoesNotExist:
        return False
