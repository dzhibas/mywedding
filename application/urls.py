from django.conf.urls import patterns, include, url
from django.contrib import admin

from weddings.views import PinView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', PinView.as_view(), name='pin1'),
    url(r'1/^$', PinView.as_view(), name='pin1'),
    url(r'2/^$', PinView.as_view(template_name='pin2.html'), name='pin2'),
    url(r'^admin/', include(admin.site.urls)),
)
