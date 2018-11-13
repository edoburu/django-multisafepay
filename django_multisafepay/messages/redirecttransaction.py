import hashlib

from .base import XmlRequest, XmlResponse


class RedirectTransaction(XmlRequest):
    """
    The message to start a checkout, using the Connect method.
    """
    xml_name = 'redirecttransaction'
    xml_fields = (
        'merchant',
        'customer',
        'google_analytics',
        'transaction',
        'plugin',
        'signature',
    )

    def __init__(self, merchant, transaction, customer, plugin=None, google_analytics=None):
        """
        :type merchant: Merchant
        :type transaction: Transaction
        :type customer: Customer
        :type google_analytics: GoogleAnalytics
        """
        self.merchant = merchant
        self.transaction = transaction
        self.customer = customer
        self.plugin = plugin
        self.google_analytics = google_analytics

    @property
    def signature(self):
        data = '{0}{1}{2}{3}{4}'.format(
            self.transaction.amount,
            self.transaction.currency,
            self.merchant.account,
            self.merchant.site_id,
            self.transaction.id
        )
        return hashlib.md5(data.encode('UTF-8')).hexdigest()


class RedirectTransactionReply(XmlResponse):
    """
    Reply from a redirecttransaction call.
    """

    def __init__(self, id, payment_url):
        """
        :param id: ID of the session
        :param payment_url: The URL to redirect to.
        """
        self.id = id
        self.payment_url = payment_url

    @classmethod
    def get_class_kwargs(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        transaction = xml.find('transaction')
        return dict(
            id=transaction.find('id').text,
            payment_url=transaction.find('payment_url').text,
        )
