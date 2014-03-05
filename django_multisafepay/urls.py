from django.conf.urls import patterns, url
from .views import NotificationView


urlpatterns = patterns('',
    url(r'^notify/$', NotificationView.as_view(), name='notification_url'),
)
