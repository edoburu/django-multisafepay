from .base import XmlObject, escape


class Transaction(XmlObject):
    """
    Transaction data
    """
    xml_name = 'transaction'
    xml_fields = (
        'id',
        'currency',
        'amount',
        'description',
        'var1',    # custom var 1
        'var2',    # custom var 2
        'var3',    # custom var 3
        'items',
        'manual',
        'daysactive',
        # 'gateway' added manually
    )

    def __init__(self, id, currency=None, amount=None, description=None, items=None, manual=None, daysactive=None, gateway=None, gateway_issuer=None, var1=None, var2=None, var3=None):
        """
        :param currency: Currency, e.g. "EUR", "USD"
        :param amount: Value in cents
        :type amount: int
        :param items: HTML text for items, e.g. ``'<br/><ul><li>1 x Item1</li><li>2 x Item2</li></ul>'``.
        :param items: str
        :param manual: Typically ``False``.
        :type manual: bool
        :param var1: Custom variable, to be returned at the callback.
        :param var2: Custom variable, to be returned at the callback.
        :param var3: Custom variable, to be returned at the callback.
        """
        self.id = id
        self.currency = currency
        self.amount = int(amount) if amount else None
        self.description = description
        self.items = items
        self.manual = manual
        self.daysactive = daysactive
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
        self.gateway = gateway
        self.gateway_issuer = gateway_issuer

    def get_xml_children(self):
        lines = super(Transaction, self).get_xml_children()
        if self.gateway is not None:
            # Add issuer attribute to the gateway tag
            issuer = u' issuer="{0}"'.format(escape(self.gateway_issuer)) if self.gateway_issuer else u''
            lines.append(u'<gateway{0}>{1}</gateway>'.format(issuer, escape(self.gateway)))
        return lines


class CheckoutSettings(XmlObject):
    """"
    Passing checkout sessions to the :class:`CheckoutTransaction` class.
    """
    xml_name = 'checkout-settings'
    xml_fields = (
        'use-shipping-notification',
    )

    def __init__(self, use_shipping_notification):
        super(CheckoutSettings, self).__init__()
        self.use_shipping_notification = bool(use_shipping_notification)


class GoogleAnalytics(XmlObject):
    """
    Passing analytics tracker to the payment pages.
    """
    xml_name = 'google-analytics'
    xml_fields = (
        'account',
    )

    def __init__(self, account):
        super(GoogleAnalytics, self).__init__()
        self.account = account
