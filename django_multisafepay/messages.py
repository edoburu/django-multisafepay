"""
The messages that the API sends to the MultiSafepay gateway.
These classes are only used by the client internally.
"""
import hashlib
from django_multisafepay import __version__ as package_version
from django_multisafepay import values


class MessageObject(values.XmlObject):
    """
    A root XML node.
    """
    def to_xml(self):
        lines = self.get_xml_children()
        return u'<?xml version="1.0" encoding="UTF-8"?>\n' \
               u'<{0} ua="django-multisafepay {1}>{2}</{0}>'.format(self.xml_name, package_version, u''.join(lines))


def _create_signature(merchant, transaction):
    """
    Create the signature.
    """
    data = '{0}{1}{2}{3}{4}'.format(
        transaction.amount,
        transaction.currency,
        merchant.account,
        merchant.site_id,
        transaction.id
    )
    return hashlib.md5(data.encode('utf-8')).hexdigest()


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

    def __init__(self, merchant, customer, customer_delivery, transaction, cart=None, fields=None, plugin=None, checkout_settings=None, google_analytics=None):
        """
        :type merchant: Merchant
        :type customer: Customer
        :type customer_delivery: CustomerDelivery
        :type plugin: Plugin
        :type google_analytics: GoogleAnalytics
        """
        self.merchant = merchant
        self.plugin = plugin
        self.customer = customer
        self.customer_delivery = customer_delivery
        self.cart = cart
        self.fields = fields
        self.google_analytics = google_analytics
        self.checkout_settings = checkout_settings
        self.transaction = transaction

    @property
    def signature(self):
        return _create_signature(self.merchant, self.transaction)


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



class Status(MessageObject):
    """
    The message to request a status
    """
    xml_name = 'status'
    xml_fields = (
        'merchant',
        'transaction',
    )

    def __init__(self, merchant, transaction_id):
        """
        :param merchant: The merchant, with the fields account, site_id, site_code filled in.
        :type merchant: Merchant
        """
        self.merchant = values.Merchant(
            # Only these fields are required:
            account = merchant.account,
            site_id = merchant.site_id,
            site_code = merchant.site_secure_code,
        )
        self.transaction = values.Transaction(id=transaction_id)


class StatusReply(object):
    """
    Reply from a status call.
    """
    def __init__(self, ewallet, customer, customer_delivery, transaction, payment_details, checkoutdata):
        self.ewallet = ewallet
        self.customer = customer
        self.customer_delivery = customer_delivery
        self.transaction = transaction
        self.payment_details = payment_details
        self.checkoutdata = checkoutdata

    STATUS_INITIALIZED = "initialized" # waiting
    STATUS_COMPLETED = "completed"     # payment complete
    STATUS_WAITING = "uncleared"       # waiting (credit cards or direct debit)
    STATUS_CANCELLED = "void"          # canceled
    STATUS_DECLINED = "declined"       # declined
    STATUS_REFUNDED = "refunded"       # refunded
    STATUS_EXPIRED = "expired"         # expired

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        return cls(
            ewallet=values.Ewallet.from_xml(xml.find('ewallet')),
            customer=values.Customer.from_xml(xml.find('customer')),
            customer_delivery=values.CustomerDelivery.from_xml(xml.find('customer-delivery')),
            transaction=values.Transaction.from_xml(xml.find('transaction')),
            paymentdetails=values.PaymentDetails.from_xml(xml.find('paymentdetails')),
            checkoutdata=None  # TODO: not implemented yet. Contains <shopping-cart>, <order-adjustment>
        )

    @property
    def status_code(self):
        return self.ewallet.status
