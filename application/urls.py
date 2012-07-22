from django.conf.urls import patterns, include, url
from django.contrib import admin

from weddings.views import Pin1View, Pin2View

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Pin1View.as_view(), name='pin1'),
    url(r'^1/$', Pin1View.as_view(), name='pin1'),
    url(r'^2/$', Pin2View.as_view(), name='pin2'),
    url(r'^admin/', include(admin.site.urls)),
)
