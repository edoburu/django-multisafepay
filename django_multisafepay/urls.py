from django.conf.urls import patterns, url
from .views import OrderNotifyView


urlpatterns = patterns('',
    url(r'^notify/$', OrderNotifyView.as_view(), name='notification_url'),
)
