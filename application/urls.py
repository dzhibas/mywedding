from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from weddings.views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^answer/(?P<person_id>\d+)/(?P<answer_id>\d+)/$', RsvpAnswerView.as_view(), name='answer'),
    url(r'^a/(?P<person_id>\d+)/(?P<answer_id>\d+)/$', answer, name='answer_ajax'),
    url(r'^p/(?P<choice_id>\d+)/$', poll_answer, name='poll_ajax'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^l/$', 'weddings.i18n.set_language'),
    url(r'^$', IndexRedirectView.as_view(), name="index")
)

urlpatterns += i18n_patterns('',
    url(r'^1/$', Pin1View.as_view(), name='pin1'),
    url(r'^2/$', Pin2View.as_view(), name='pin2'),
    url(r'^invitation/$', InvitationView.as_view(), name='invitation'),
    url(r'^friends/$', FriendsView.as_view(), name='friends'),
    url(r'^story/$', StoryView.as_view(), name='story'),
)
