# coding=utf-8

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from weddings.models import Invitation
from django.utils.translation import ugettext as _


class Pin2View(TemplateView):
    template_name = "pin2.html"
    guest_list = None
    logged_in_guest = None

    def get(self, request, *args, **kwargs):
        if 'logged_in_guest' in request.COOKIES:
            self.logged_in_guest = request.COOKIES['logged_in_guest']

        if 'pin_provided' in request.session and 'logged_pin' in request.session:
            invitation = self.check_pin(request.session['logged_pin'])
            if invitation != False:
                guests = invitation.weddingguest_set.all()
                self.guest_list = guests
                return super(Pin2View, self).get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('pin1'))

    # todo - check if lonely guest dont want to get friend
    def post(self, request, *args, **kwargs):
        if 'pin_provided' not in request.session and 'logged_pin' not in request.session:
            return HttpResponseRedirect(reverse('pin1'))

        invitation = self.check_pin(request.session['logged_pin'])
        if invitation == False:
            return HttpResponseRedirect(reverse('pin1'))

        real_guest_count = len(invitation.weddingguest_set.filter(invited=False))
        if real_guest_count < 2:
            # Two cases. When there is only one WeddingGuest (invited = False)
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

            request.session['logged_in_quest'] = guest_id

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
        return context
