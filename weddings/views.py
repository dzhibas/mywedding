from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse


class PinView(TemplateView):
    template_name = "pin1.html"

    def post(self, request):
        return HttpResponseRedirect(reverse('pin2'))

    def get_context_data(self, **kwargs):
        context = super(PinView, self).get_context_data(**kwargs)
        return context
