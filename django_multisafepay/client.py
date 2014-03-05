"""
API calls to the payment gateway webservice
"""
import logging
import requests
from xml.etree import ElementTree
from django_multisafepay import __version__ as package_version
from django_multisafepay import appsettings, messages
from django_multisafepay.exceptions import MultiSafepayServerException, MultiSafepayException
from django_multisafepay.values import Merchant, Plugin

logger = logging.getLogger(__name__)


URL_TEST = "https://testapi.multisafepay.com/ewx/"
URL_LIVE = "https://api.multisafepay.com/ewx/"


class MultiSafepayClient(object):
    """
    The MultiSafepay API client.
    """

    def __init__(self, merchant=None, plugin=None, is_test=None):
        """
        Provide account details to call the service.

        :param merchant: Custom merchant settings. By default the settings file is read.
        :type merchant: Merchant
        :param plugin: Custom metadata about the shop-plugin that is used.
        :type plugin: Plugin
        :param is_test: Whether to use testing mode. Using ``None`` defaults to the defined setting value.
        :type is_test: bool
        """
        self.merchant = merchant or Merchant()
        self.plugin = plugin
        self.is_test = is_test if is_test is not None else appsettings.MULTISAFEPAY_TESTING


    @property
    def api_url(self):
        return URL_TEST if self.is_test else URL_LIVE


    def start_checkout(self, transaction, customer, customer_delivery, cart=None, fields=None, checkout_settings=None, google_analytics=None):
        """
        Start the checkout (Fast-Checkout method)

        :type transaction: Transaction
        :type customer: Customer
        :type customer_delivery: CustomerDelivery
        :type google_analytics: GoogleAnalytics
        :rtype: CheckoutTransactionReply
        """
        xml = self._call(messages.CheckoutTransaction(
            merchant=self.merchant,
            customer=customer,
            customer_delivery=customer_delivery,
            transaction=transaction,
            cart=cart,
            fields=fields,
            plugin=self.plugin,
            checkout_settings=checkout_settings,
            google_analytics=google_analytics
        ))

        # Report errors
        if xml.attrib['result'] != 'ok':
            ex = MultiSafepayServerException.from_xml(xml)
            logger.error(u"Failed to start transaction {0}: code={1}, description={2}".format(transaction.id, ex.code, ex.description))
            raise ex

        return messages.CheckoutTransactionReply.from_xml(xml)


    def status(self, transaction_id):
        """
        Request the status of a transaction.
        """
        xml = self._call(messages.Status(self.merchant, transaction_id))

        # Report errors
        if xml.attrib['result'] != 'ok':
            ex = MultiSafepayServerException.from_xml(xml)
            logger.error(u"Failed to fetch status for transaction {0}: code={1}, description={2}".format(transaction_id, ex.code, ex.description))
            raise ex

        return messages.StatusReply.from_xml(xml)


    def _call(self, message):
        """
        Make the call to the server
        :rtype: xml.etree.ElementTree.Element
        """
        postdata = message.to_xml()
        logger.debug(u"sending to {0}:\n{1}".format(self.api_url, postdata))

        response = requests.post(
            self.api_url,
            headers={
                'Content-Type': 'text/xml',
                'Accept': 'text/xml; charset=utf-8',
                'User-Agent': 'django-multisafepay/{0}'.format(package_version),
            },
            data=postdata.encode('utf-8'),
            allow_redirects=False,
            verify=True
        )

        # Raise on invalid status
        if response.status_code >= 400:
            logger.error(u"http failed: {0} {1}".format(response.status_code, response.content))
            response.raise_for_status()

        if '/xml' not in response.headers['Content-Type']:
            raise MultiSafepayException("Received invalid content-type: {0}".format(response.headers['Content-Type']))

        logger.debug(u"http succeeded: {0}".format(response.content))

        xml = ElementTree.fromstring(response.content)
        return xml
