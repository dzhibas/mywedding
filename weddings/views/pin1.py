# coding=utf-8

from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from weddings.models import Invitation, CodeGuess
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
from django.utils.translation import check_for_language, activate


class Pin1View(TemplateView):
    template_name = "pin1.html"
    error = False
    pin = None

    def get(self, request, *args, **kwargs):
        if 'pin_provided' in request.session and 'logged_pin' in request.session:
            invitation = self.check_pin(request.session['logged_pin'])
            if invitation != False:
                activate(invitation.invitation_language)
                messages.success(request, _(u"Kodas patikrintas"))
                return HttpResponseRedirect(reverse('pin2'))

        if 'post_pin' in request.session:
            self.pin = request.session['post_pin'].strip()

        response = super(Pin1View, self).get(request, *args, **kwargs)
        return response

    def post(self, request):
        if 'pin' not in request.POST or request.POST['pin'].strip() == '':
            messages.error(request, _(u'Nurodykite kodą'))
            # log empty try of guess
            CodeGuess.objects.create(ip=self.ip_addr(request), guess_code='')
            return HttpResponseRedirect(reverse('pin1'))

        request.session['post_pin'] = request.POST['pin'].strip()

        # check if there is not too much tries
        guesses = CodeGuess.objects.filter(when_tried__gt=datetime.today() - timedelta(hours=3), \
                                            ip=self.ip_addr(request))
        if len(guesses) > 4:
            CodeGuess.objects.create(ip=self.ip_addr(request), guess_code=request.POST['pin'])
            messages.error(request, _(u'Prisižaidėt. Dabar tris valandas spėlioti nebegalit'))
            return HttpResponseRedirect(reverse('pin1'))

        # log guess trying
        CodeGuess.objects.create(ip=self.ip_addr(request), guess_code=request.POST['pin'])

        success_response = HttpResponseRedirect(reverse('pin2'))

        try:
            obj = Invitation.objects.get(invite_code__iexact=request.POST['pin'])

            # setting application language to invitation language
            invitation_language = obj.invitation_language

            if invitation_language and check_for_language(invitation_language):
                activate(invitation_language)
                success_response = HttpResponseRedirect(reverse('pin2'))
                if hasattr(request, 'session'):
                    request.session['django_language'] = invitation_language
                else:
                    success_response.set_cookie(settings.LANGUAGE_COOKIE_NAME, invitation_language)

            request.session['logged_pin'] = obj.invite_code
            request.session['pin_provided'] = True
            messages.success(request, _('Kodas patvirtintas'))
        except Invitation.DoesNotExist:
            messages.error(request, _(u'Tokio kodo nėra'))
            return HttpResponseRedirect(reverse('pin1'))
        except Invitation.MultipleObjectsReturned:
            messages.error(request, _(u'Tokio kodo nėra'))
            return HttpResponseRedirect(reverse('pin1'))

        return success_response

    def get_context_data(self, **kwargs):
        context = super(Pin1View, self).get_context_data(**kwargs)
        context['error'] = self.error
        context['pin'] = self.pin
        return context

    def check_pin(self, pin):
        try:
            return Invitation.objects.get(invite_code__iexact=pin)
        except Invitation.DoesNotExist:
            return False
        except Invitation.MultipleObjectsReturned:
            return False

    def ip_addr(self, request):
        if 'HTTP_X_REAL_IP' not in request.META:
            return request.META['REMOTE_ADDR']
        else:
            return request.META['HTTP_X_REAL_IP']
