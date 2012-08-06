from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from weddings.models import Invitation


class Pin2View(TemplateView):
    template_name = "pin2.html"
    guest_list = None

    def get(self, request, *args, **kwargs):
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

        if 'guest' not in request.POST or request.POST['guest'] == '':
            messages.error(request, 'Please select one person')
            return HttpResponseRedirect(reverse('pin2'))

        guests = invitation.weddingguest_set.all()
        allowed_guest_ids = [guest.id for guest in guests]

        guest_id = int(request.POST['guest'])

        if guest_id not in allowed_guest_ids:
            messages.error(request, 'No chance you can select this person')
            return HttpResponseRedirect(reverse('pin2'))

        request.session['logged_in_quest'] = guest_id

        return HttpResponseRedirect(reverse('invitation'))

    def check_pin(self, pin):
        try:
            return Invitation.objects.get(invite_code__iexact=pin)
        except Invitation.DoesNotExist:
            return False

    def get_context_data(self, **kwargs):
        context = super(Pin2View, self).get_context_data(**kwargs)
        context['guests'] = self.guest_list
        context['guest_count'] = len(self.guest_list)
        return context
