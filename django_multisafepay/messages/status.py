from django_multisafepay.data import Customer, CustomerDelivery, Transaction, Merchant
from django_multisafepay.data.status import Ewallet, PaymentDetails
from .base import MessageObject


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
        self.merchant = Merchant(
            # Only these fields are required:
            account = merchant.account,
            site_id = merchant.site_id,
            site_code = merchant.site_secure_code,
        )
        self.transaction = Transaction(id=transaction_id)


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
            ewallet=Ewallet.from_xml(xml.find('ewallet')),
            customer=Customer.from_xml(xml.find('customer')),
            customer_delivery=CustomerDelivery.from_xml(xml.find('customer-delivery')),
            transaction=Transaction.from_xml(xml.find('transaction')),
            paymentdetails=PaymentDetails.from_xml(xml.find('paymentdetails')),
            checkoutdata=None  # TODO: not implemented yet. Contains <shopping-cart>, <order-adjustment>
        )

    @property
    def status_code(self):
        return self.ewallet.status
