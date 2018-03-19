from django_multisafepay.data import Customer

from .base import Price, XmlObject


class Ewallet(XmlObject):
    """
    The EWallet element in the status reply.
    It contains the status code.
    """
    xml_name = 'ewallet'
    xml_fields = (
        'id',
        'fastcheckout',
        'status',
        'created',
        'modified',
        'reason',
        'reasoncode',
    )

    def __init__(self, id, status, fastcheckout, created, modified, reason=None, reasoncode=None):
        self.id = id
        self.status = status
        self.fastcheckout = bool(fastcheckout is True or fastcheckout == 'YES')
        self.created = created
        self.modified = modified
        self.reason = reason
        self.reasoncode = reasoncode


class CustomerStatus(Customer):
    """
    A customer with additional fields.
    """
    xml_fields = Customer.xml_fields + (
        'amount',
        'currency',
        'account',
        'phone1',
        'phone2',
        'countryname'
    )

    def __init__(self, *args, **kwargs):
        self.amount = kwargs.pop('amount')
        self.currency = kwargs.pop('currency')
        self.account = kwargs.pop('account')
        self.phone1 = kwargs.pop('phone1')
        self.phone2 = kwargs.pop('phone2')
        self.countryname = kwargs.pop('countryname')
        super(CustomerStatus, self).__init__(*args, **kwargs)


class PaymentDetails(XmlObject):
    """
    The payment details in the status reply
    """
    xml_name = 'paymentdetails'
    xml_fields = (
        'type',
        'accountid',
        'accountholdername',
        'externaltransactionid',
    )

    def __init__(self, type, accountid, accountholdername, externaltransactionid):
        self.type = type
        self.accountid = accountid
        self.accountholdername = accountholdername
        self.externaltransactionid = externaltransactionid


class CheckoutData(XmlObject):
    """
    The checkout data in the status reply
    """
    xml_name = 'checkoutdata'
    xml_fields = (
        'shopping-cart',
        'order-adjustment',
        'order-total',
        'custom-fields',
    )

    def __init__(self, order_total, shopping_cart=None, order_adjustment=None, custom_fields=None):
        self.order_total = order_total
        self.shopping_cart = shopping_cart
        self.order_adjustment = order_adjustment
        self.custom_fields = custom_fields

    @classmethod
    def get_class_kwargs(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        return dict(
            order_total=Price.from_xml(xml.find('order-total')),
            order_adjustment=OrderAdjustment.from_xml(xml.find('order-adjustment')),
            shopping_cart=None,
            custom_fields=None,
            # TODO: all other objects are currently ignored. (shopping-cart, custom-fields)
        )


class TransactionStatus(XmlObject):
    """
    Information about a transaction, as returned by the status call..
    """
    xml_name = 'transaction'
    xml_fields = (
        'id',
        'recurringid',
        'currency',
        'amount',
        'cost',
        'description',
        'var1',    # custom var 1
        'var2',    # custom var 2
        'var3',    # custom var 3
        'items',
        'amountrefunded',
    )

    def __init__(self, id, recurringid, currency, amount, cost, description, var1=None, var2=None, var3=None, items=None, amountrefunded=None):
        self.id = id
        self.recurringid = recurringid
        self.currency = currency
        self.amount = amount
        self.cost = cost
        self.description = description
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
        self.items = items
        self.amountrefunded = amountrefunded


class OrderAdjustment(XmlObject):
    """
    The order adjustment in the CheckoutData of the status reply.
    """
    xml_name = 'order-adjustment'
    xml_fields = (
        'shipping',
        'adjustment-total',
        'total-tax'
    )

    def __init__(self, shipping, adjustment_total, total_tax):
        self.shipping = shipping
        self.adjustment_total = adjustment_total
        self.total_tax = total_tax

    @classmethod
    def get_class_kwargs(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        return dict(
            shipping=None,   # TODO: not implemented
            adjustment_total=Price.from_xml(xml.find('adjustment-total')),
            total_tax=Price.from_xml(xml.find('total-tax')),
        )
