from django.conf.urls import patterns, include, url
from django.contrib import admin

from weddings.views import Pin1View, Pin2View, InvitationView, RsvpAnswerView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Pin1View.as_view(), name='pin1'),
    url(r'^1/$', Pin1View.as_view(), name='pin1'),
    url(r'^2/$', Pin2View.as_view(), name='pin2'),
    url(r'^invitation/$', InvitationView.as_view(), name='invitation'),
    url(r'^answer/(?P<person_id>\d+)/(?P<answer_id>\d+)/$', RsvpAnswerView.as_view(), name='answer'),
    url(r'^admin/', include(admin.site.urls)),
    url('^markdown/', include('django_markdown.urls')),
)
