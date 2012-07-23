from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from weddings.models import Invitation, CodeGuess
from datetime import datetime, timedelta


class Pin1View(TemplateView):
    template_name = "pin1.html"

    def get(self, request, *args, **kwargs):
        if 'pin_provided' in request.session and 'logged_pin' in request.session:
            if self.check_pin(request.session['logged_pin']):
                messages.success(request, 'Already verified')
                return HttpResponseRedirect(reverse('pin2'))

        response = super(Pin1View, self).get(request, *args, **kwargs)
        return response

    def post(self, request):
        if 'pin' not in request.POST or request.POST['pin'].strip() == '':
            messages.error(request, 'No pin provided')
            # log empty try of guess
            CodeGuess.objects.create(ip=self.ip_addr(request), guess_code='')
            return HttpResponseRedirect(reverse('pin1'))

        # check if there is not too much tries
        guesses = CodeGuess.objects.filter(when_tried__gt=datetime.today() - timedelta(hours=3), \
                                            ip=self.ip_addr(request))
        if len(guesses) > 4:
            CodeGuess.objects.create(ip=self.ip_addr(request), guess_code=request.POST['pin'])
            messages.error(request, 'Too many tries. You locked for next 3 hours')
            return HttpResponseRedirect(reverse('pin1'))

        # log guess trying
        CodeGuess.objects.create(ip=self.ip_addr(request), guess_code=request.POST['pin'])

        try:
            obj = Invitation.objects.get(invite_code=request.POST['pin'])
            request.session['logged_pin'] = obj.invite_code
            request.session['pin_provided'] = True
            messages.success(request, 'Pin verified')
        except Invitation.DoesNotExist:
            messages.error(request, 'No such pin')
            return HttpResponseRedirect(reverse('pin1'))

        return HttpResponseRedirect(reverse('pin2'))

    def get_context_data(self, **kwargs):
        context = super(Pin1View, self).get_context_data(**kwargs)
        return context

    def check_pin(self, pin):
        try:
            Invitation.objects.get(invite_code=pin)
            return True
        except Invitation.DoesNotExist:
            return False

    def ip_addr(self, request):
        if 'REMOTE_ADDR' in request.META:
            return request.META['REMOTE_ADDR']
