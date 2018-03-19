from django.conf.urls import url

from .views import NotificationView

urlpatterns = [
    url(r'^notify/$', NotificationView.as_view(), name='notification_url'),
]
