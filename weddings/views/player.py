from django.views.generic import TemplateView


class PlayerView(TemplateView):
    template_name = "player.html"
