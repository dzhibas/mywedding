# coding=utf-8

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from weddings.models import Invitation, WeddingGuest
from django.utils.translation import ugettext as _


class Pin2View(TemplateView):
    template_name = "pin2.html"
    guest_list = None
    logged_in_guest = 0
    invited_guest_id = ""
    invited_guest_fullname = ""

    def get(self, request, *args, **kwargs):
        if 'logged_in_guest' in request.COOKIES:
            self.logged_in_guest = request.COOKIES['logged_in_guest']

        if 'pin_provided' in request.session and 'logged_pin' in request.session:
            invitation = self.check_pin(request.session['logged_pin'])
            if invitation != False:
                guests = invitation.weddingguest_set.filter(invited=False)
                self.guest_list = guests
                invited_guests = invitation.weddingguest_set.filter(invited=True)
                if len(invited_guests) > 0:
                    invitation_guest = invited_guests[0]
                    self.invited_guest_id = invitation_guest.pk
                    self.invited_guest_fullname = invitation_guest.full_name
                return super(Pin2View, self).get(request, *args, **kwargs)

        # in case something went worng
        return HttpResponseRedirect(reverse('pin1'))

    # todo - check if lonely guest dont want to get friend
    def post(self, request, *args, **kwargs):
        if 'pin_provided' not in request.session and 'logged_pin' not in request.session:
            return HttpResponseRedirect(reverse('pin1'))

        invitation = self.check_pin(request.session['logged_pin'])
        if invitation == False:
            return HttpResponseRedirect(reverse('pin1'))

        real_guests = invitation.weddingguest_set.filter(invited=False)
        real_guest_count = len(real_guests)
        if real_guest_count < 2:
            # Two cases. When there is only one WeddingGuest (invited = False)

            # get already invited guests
            invited_guests = invitation.weddingguest_set.filter(invited=True)

            # check if name was entered
            if 'invitation_guest_fullname' in request.POST and request.POST['invitation_guest_fullname'] != '':
                # guest fullname was provided
                provided_full_name = request.POST['invitation_guest_fullname'].strip()
                first_name = ""
                last_name = ""
                if len(provided_full_name.split(' ')) == 2:
                    first_name, last_name = provided_full_name.split(' ')
                elif len(provided_full_name.split(' ')) > 2:
                    first_name, last_name = provided_full_name.split(' ')[:2]
                else:
                    first_name = provided_full_name.strip()

                # if there is already invited guests lets update their fullname with provided now
                if len(invited_guests) > 0:
                    # save existing
                    invited_guest = invited_guests[0]
                    invited_guest.first_name = first_name
                    invited_guest.last_name = last_name
                    invited_guest.invited_by = real_guests[0]
                    invited_guest.save()
                else:
                    # create a new one
                    new_guest = WeddingGuest()
                    new_guest.invited = True
                    new_guest.invitation = invitation
                    new_guest.invited_by = real_guests[0]
                    new_guest.first_name = first_name
                    new_guest.last_name = last_name
                    new_guest.save()

            request.session['logged_in_guest'] = real_guests[0].pk

            response = HttpResponseRedirect(reverse('invitation'))

        else:
            # Second case. When it is more than one WeddingGuest (invited = False)
            if 'guest' not in request.POST or request.POST['guest'] == '':
                messages.error(request, _(u"Pasirinkite svečią iš pateikto sąrašo"))
                return HttpResponseRedirect(reverse('pin2'))

            guests = invitation.weddingguest_set.all()
            allowed_guest_ids = [guest.id for guest in guests]

            guest_id = int(request.POST['guest'])

            if guest_id not in allowed_guest_ids:
                messages.error(request, _(u"Oi oi oi, tu negali pasirinkti šio svečio. Ar tikrai tai tu ?"))
                return HttpResponseRedirect(reverse('pin2'))

            request.session['logged_in_guest'] = guest_id

            response = HttpResponseRedirect(reverse('invitation'))
            response.set_cookie('logged_in_guest', guest_id)

        return response

    def check_pin(self, pin):
        try:
            return Invitation.objects.get(invite_code__iexact=pin)
        except Invitation.DoesNotExist:
            return False

    def get_context_data(self, **kwargs):
        context = super(Pin2View, self).get_context_data(**kwargs)
        context['guests'] = self.guest_list
        context['guest_count'] = len(self.guest_list)
        context['logged_in_guest'] = int(self.logged_in_guest)
        context['invitation_guest_id'] = self.invited_guest_id
        context['invitation_guest_fullname'] = self.invited_guest_fullname
        return context
