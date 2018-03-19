import logging

from django.db import transaction
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django_multisafepay.client import MultiSafepayClient
from django_multisafepay.signals import order_status_updated

logger = logging.getLogger(__name__)

# New transaction support in Django 1.6
try:
    transaction_atomic = transaction.atomic
except AttributeError:
    transaction_atomic = transaction.commit_on_success


class NotificationView(View):
    """
    View to be called by MultiSafepay when a status update occured.
    """
    return_link_text = _('Return to webshop')
    client_class = MultiSafepayClient

    def get(self, request, *args, **kwargs):
        """
        Handle the incoming notification request.
        """
        try:
            self.transaction_id = request.GET['transactionid']
        except KeyError:
            return HttpResponse("missing transactionid", status=403)
        self.type = request.GET.get('type')

        # Request the new status from the server.
        client = self.get_client()
        statusreply = client.status(self.transaction_id)

        # Let the project update the status
        if not order_status_updated.has_listeners():
            logger.warning("No listeners for `order_status_updated` signal!")
        else:
            with transaction_atomic():
                order_status_updated.send(self.__class__, statusreply=statusreply, request=self.request)

        if self.type == 'initial':
            # displayed at the last page of the transaction process (if no redirect_url is set)
            return self.render_to_response()
        else:
            # MultiSafepay back-end expects an "ok" if no error occurred
            return HttpResponse('ok')

    def get_client(self):
        """
        Return the MultiSafepay API client.
        This method can be overwritten to create a custom client, with other merchant parameters for example.
        """
        return self.client_class()

    def render_to_response(self):
        """
        Render the response when no redirect_url is set.
        """
        url = self.request.build_absolute_uri('/')
        return HttpResponse(format_html(u'<a href="{0}">{1}</a>', url, self.return_link_text))
