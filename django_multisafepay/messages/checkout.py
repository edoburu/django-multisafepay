import hashlib
from .base import MessageObject


class CheckoutTransaction(MessageObject):
    """
    The message to start a checkout
    """
    xml_name = 'checkouttransaction'
    xml_fields = (
        'merchant',
        'plugin',
        'customer',
        'customer_delivery',
        'cart',             # TODO: Cart data model not implemented yet   (uses Google Checkout Cart format)
        'fields',           # TODO: Fields data model not implemented yet (for custom form fields)
        'google_analytics',
        'checkout_settings',
        'transaction',
        'signature',
    )

    def __init__(self, merchant, transaction, customer, customer_delivery=None, cart=None, fields=None, plugin=None, checkout_settings=None, google_analytics=None):
        """
        :type merchant: Merchant
        :type customer: Customer
        :type customer_delivery: CustomerDelivery
        :type cart: Cart
        :type plugin: Plugin
        :type google_analytics: GoogleAnalytics
        """
        self.merchant = merchant
        self.plugin = plugin
        self.transaction = transaction
        self.customer = customer
        self.customer_delivery = customer_delivery
        self.cart = cart
        self.fields = fields
        self.google_analytics = google_analytics
        self.checkout_settings = checkout_settings

    @property
    def signature(self):
        data = '{0}{1}{2}{3}{4}'.format(
            self.transaction.amount,
            self.transaction.currency,
            self.merchant.account,
            self.merchant.site_id,
            self.transaction.id
        )
        return hashlib.md5(str(data)).hexdigest()


class CheckoutTransactionReply(object):
    """
    Reply from a start_transaction call.
    """
    def __init__(self, id, payment_url):
        """
        :param id: ID of the session
        :param payment_url: The URL to redirect to.
        """
        self.id = id
        self.payment_url = payment_url

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        transaction = xml.find('transaction')
        return cls(
            id=transaction.find('id').text,
            payment_url=transaction.find('payment_url').text
        )
