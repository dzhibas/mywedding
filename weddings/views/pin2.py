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

    def check_pin(self, pin):
        try:
            return Invitation.objects.get(invite_code=pin)
        except Invitation.DoesNotExist:
            return False

    def get_context_data(self, **kwargs):
        context = super(Pin2View, self).get_context_data(**kwargs)
        context['guests'] = self.guest_list
        context['guest_count'] = len(self.guest_list)
        return context