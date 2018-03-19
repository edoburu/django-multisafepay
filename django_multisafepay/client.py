"""
API calls to the payment gateway webservice
"""
import logging
from xml.etree import ElementTree

import requests
from django_multisafepay import __version__ as package_version
from django_multisafepay import appsettings, messages
from django_multisafepay.data import Merchant, Plugin
from django_multisafepay.data.gateway import GatewayCustomer
from django_multisafepay.exceptions import MultiSafepayException, MultiSafepayServerException

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
        self.plugin = plugin or Plugin()
        self.is_test = is_test if is_test is not None else appsettings.MULTISAFEPAY_TESTING

    @property
    def api_url(self):
        return URL_TEST if self.is_test else URL_LIVE

    def _call(self, message, response_class=None):
        """
        Make the call to the server
        :rtype: :class:`xml.etree.ElementTree.Element` | response_class
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

        # Fix MultiSafepay response header error.
        # Encoding is only specified in the <?xml preamble, not in the HTTP Content-Type header.
        # "response.text" parses the response in the proper encoding format.
        # "response.content" is the raw content, that's being sent to the XML parser.
        response.encoding = 'utf-8'
        logger.debug(u"http succeeded: {0}".format(response.text))

        xml = ElementTree.fromstring(response.content)  # parser=ElementTree.XMLParser(encoding=response.encoding))  # Python 2.6 doesn't support this.

        if xml.attrib['result'] != 'ok':
            ex = MultiSafepayServerException.from_xml(xml)
            logger.error(u"Request <%s> to MultiSafePay failed: code=%s, description=%s", message.xml_name, ex.code, ex.description)
            raise ex

        if response_class is not None:
            return response_class.from_xml(xml)
        else:
            return xml

    def _transaction_call(self, message, response_class=None):
        """
        A variant of the standard ``_call()`` that logs the transaction ID on errors.

        :type message: RedirectTransaction
        :type response_class: RedirectTransactionReply
        :rtype: RedirectTransactionReply
        """
        try:
            return self._call(message, response_class=response_class)
        except MultiSafepayServerException as e:
            # Be more verbose in the logs.
            logger.error(u"Failed to start transaction %s: code=%s, description=%s", message.transaction.id, e.code, e.description)
            if e.code == e.CODE_INVALID_TRANSACTION_ID:
                # Mention transaction ID in exception message
                raise MultiSafepayServerException(e.code, u"{0} ({1})".format(e.description, message.transaction.id))
            raise

    def start_checkout(self, transaction, customer, customer_delivery=None, cart=None, fields=None, checkout_settings=None, google_analytics=None):
        """
        Start the checkout (Fast-Checkout method)

        :param transaction: The information about the transaction.
        :type transaction: Transaction
        :param customer: The information about the customer.
        :type customer: Customer
        :param customer_delivery: The delivery address.
        :type customer_delivery: CustomerDelivery
        :param cart: The shopping cart.
        :type cart: Cart
        :param fields: Not supported yet.
        :param checkout_settings: Checkout sessions, only provides "use shipping notification" for now.
        :type checkout_settings: CheckoutSettings
        :param google_analytics: Analytics to use on the payment page.
        :type google_analytics: GoogleAnalytics
        :rtype: CheckoutTransactionReply
        """
        request = messages.CheckoutTransaction(
            merchant=self.merchant,
            transaction=transaction,
            customer=customer,
            customer_delivery=customer_delivery,
            cart=cart,
            fields=fields,
            plugin=self.plugin,
            checkout_settings=checkout_settings,
            google_analytics=google_analytics
        )

        return self._transaction_call(request, response_class=messages.CheckoutTransactionReply)

    def status(self, transaction_id):
        """
        Request the status of a transaction.
        :rtype: StatusReply
        """
        request = messages.Status(self.merchant, transaction_id)
        try:
            return self._call(request, response_class=messages.StatusReply)
        except MultiSafepayServerException as e:
            # Be more verbose in the logs.
            logger.error(u"Failed to fetch status for transaction %s: code=%s, description=%s", transaction_id, e.code, e.description)
            raise

    def gateways(self, locale, country):
        """
        Request all available gateways (Connect method)

        :param locale: Language code, e.g. en_US
        :param country: The 2-digit country code, in ISO 3166
        :rtype: GatewaysReply
        """
        request = messages.Gateways(
            merchant=self.merchant,
            customer=GatewayCustomer(
                locale=locale,
                country=country,
            )
        )

        return self._call(request, response_class=messages.GatewaysReply)

    def redirect_transaction(self, transaction, customer, google_analytics=None):
        """
        Start the checkout (Connect method)

        :param transaction: The information about the transaction.
        :type transaction: Transaction
        :param customer: The information about the customer.
        :type customer: Customer
        :param google_analytics: Analytics to use on the payment page.
        :type google_analytics: GoogleAnalytics
        :rtype: CheckoutTransactionReply
        """
        request = messages.RedirectTransaction(
            merchant=self.merchant,
            transaction=transaction,
            customer=customer,
            plugin=self.plugin,
            google_analytics=google_analytics
        )

        return self._transaction_call(request, response_class=messages.RedirectTransactionReply)

    def direct_transaction(self, transaction, customer, gatewayinfo, google_analytics=None):
        """
        Start the checkout (Connect method)

        :param transaction: The information about the transaction.
        :type transaction: Transaction
        :param customer: The information about the customer.
        :type customer: Customer
        :param gatewayinfo: The exact payment gateway to use.
        :type gatewayinfo: GatewayInfo
        :param google_analytics: Analytics to use on the payment page.
        :type google_analytics: GoogleAnalytics
        :rtype: CheckoutTransactionReply
        """
        request = messages.DirectTransaction(
            merchant=self.merchant,
            transaction=transaction,
            customer=customer,
            gatewayinfo=gatewayinfo,
            google_analytics=google_analytics
        )

        return self._transaction_call(request, response_class=messages.DirectTransactionReply)

    # TODO: idealissuers request
