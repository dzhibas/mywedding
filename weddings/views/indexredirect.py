from django.views.generic import RedirectView


class IndexRedirectView(RedirectView):
    url = "/lt/1/"
