"""
The data objects can be provided as parameters to the client.
"""
from xml.sax.saxutils import escape
from decimal import Decimal
from django.core.urlresolvers import reverse
from django_multisafepay import appsettings


class XmlObject(object):
    """
    Simple object to quickly generate XML messages.
    """
    xml_name = None
    xml_attrs = None
    xml_fields = ()

    def to_xml(self):
        # get xml message
        lines = self.get_xml_children()
        return u'<{0}>{1}</{0}>'.format(self.xml_name, u''.join(lines))

    def get_xml_attrs(self):
        return self.xml_attrs

    def get_xml_children(self):
        # Allow to be overwritten
        lines = []
        for field in self.xml_fields:
            value = getattr(self, field.replace('-', '_'))
            if value is not None:
                if isinstance(value, XmlObject):
                    lines.append(value.to_xml())
                else:
                    if isinstance(value, (list, tuple)):
                        tag_value = u''.join(item.to_xml() for item in value)
                    elif isinstance(value, bool):
                        return str(value).lower()
                    else:
                        tag_value = escape(value)
                    lines.append(u'<{0}>{1}</{0}>'.format(field, tag_value))
        return lines

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        if xml is None:
            return None
        return cls(**cls.get_class_kwargs(xml))

    @classmethod
    def get_class_kwargs(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        kwargs = {}
        for field in cls.xml_fields:
            node = xml.find(field)
            kwargs[field.replace('-', '_')] = None if node is None else node.text
        return kwargs



class Merchant(XmlObject):
    """
    Meta information for the webshop.
    """
    xml_name = 'marchant'
    xml_fields = (
        'account',
        'site_id',
        'site_secure_code',
        'notification_url',
        'cancel_url',
        'redirect_url',
        'close_window',
    )

    def __init__(self, account=None, site_id=None, site_code=None, notification_url=None, cancel_url=None, redirect_url=None, close_window=None):
        """
        If the account, site_id and site_code are omitted, the defaults are read from the settings file.
        """
        self.account = account or appsettings.MULTISAFEPAY_ACCOUNT_ID
        self.site_id = site_id or appsettings.MULTISAFEPAY_SITE_ID
        self.site_secure_code = site_code or appsettings.MULTISAFEPAY_SITE_CODE

        # Custom configuration
        self.notification_url = notification_url or reverse('notification_url')
        self.cancel_url = cancel_url or appsettings.MULTISAFEPAY_CANCEL_URL
        self.redirect_url = redirect_url or appsettings.MULTISAFEPAY_REDIRECT_URL
        self.close_window = close_window



class Plugin(XmlObject):
    """
    Meta information for the plugin
    """
    xml_name = 'plugin'
    xml_fields = (
        'shop',
        'shop_version',
        'plugin_version',
        'partner',
        'shop_root_url',
    )

    def __init__(self, shop=None, shop_version=None, plugin_version=None, partner=None, shop_root_url=None):
        self.shop = shop
        self.shop_version = shop_version
        self.plugin_version = plugin_version
        self.partner = partner
        self.shop_root_url = shop_root_url



class Customer(XmlObject):
    """
    Customer information
    """
    xml_name = 'customer'
    xml_fields = (
        'locale',
        'ipaddress',
        'forwardedip',
        'firstname',
        'lastname',
        'address1',
        'address2',
        'housenumber',
        'zipcode',
        'city',
        'state',
        'country',
        'phone',
        'email',
        'referrer',
        'user_agent'
    )

    def __init__(self, locale, firstname, lastname, address1, address2, housenumber, zipcode, city, state, country, phone, email, ipaddress, forwardedip, referrer, user_agent):
        """
        :param locale: Customer locale, e.g. AB_cd; the language (ISO 639) and country (ISO 3166-1)
        :param country: The 2-digit country code, in ISO 3166
        """
        self.locale = locale
        self.firstname = firstname
        self.lastname = lastname
        self.address1 = address1
        self.address2 = address2
        self.housenumber = housenumber
        self.zipcode = zipcode
        self.city = city
        self.state = state
        self.country = country
        self.phone = phone
        self.email = email

        self.ipaddress = ipaddress
        self.forwardedip = forwardedip
        self.referrer = referrer
        self.user_agent = user_agent



class CustomerDelivery(XmlObject):
    """
    Delivery address
    """
    xml_name = 'customer-delivery'
    xml_fields = (
        'firstname',
        'lastname',
        'address1',
        'address2',
        'housenumber',
        'zipcode',
        'city',
        'state',
        'country',
        'phone',
        'email',
    )

    def __init__(self, firstname, lastname, address1, address2, housenumber, zipcode, city, state, country, phone, email):
        """
        :param country: The 2-digit country code, in ISO 3166
        """
        self.firstname = firstname
        self.lastname = lastname
        self.address1 = address1
        self.address2 = address2
        self.housenumber = housenumber
        self.zipcode = zipcode
        self.city = city
        self.state = state
        self.country = country
        self.phone = phone
        self.email = email


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
        #'gateway'
    )

    def __init__(self, id, currency=None, amount=None, description=None, items=None, manual=None, daysactive=None, gateway=None, issuer=None, var1=None, var2=None, var3=None):
        """
        :type items: list
        :param currency: Currency, e.g. "EUR", "USD"
        :param amount: Value in cents
        :param items: HTML text for items, e.g. ``'<br/><ul><li>1 x Item1</li><li>2 x Item2</li></ul>'``.
        """
        self.id = id
        self.currency = currency
        self.amount = amount
        self.description = description
        self.items = items
        self.manual = manual
        self.daysactive = daysactive
        self.var1 = var1
        self.var2 = var2
        self.var3 = var3
        self.gateway = gateway
        self.issuer = issuer

    def get_xml_children(self):
        lines = super(Transaction, self).get_xml_children()
        # Add issuer attribute to the gateway tag
        issuer = u' issuer="{0}"'.format(escape(self.issuer)) if self.issuer else u''
        lines.append(u'<gateway{0}>{1}</gateway>'.format(issuer, escape(self.gateway)))
        return lines


class Ewallet(XmlObject):
    """
    The EWallet element in the status reply.
    It contains the status code.
    """
    xml_name = 'ewallet'
    xml_fields = (
        'id',
        'status',
        'created',
        'modified',
    )

    def __init__(self, id, status, created, modified):
        self.id = id
        self.status = status
        self.created = created
        self.modified = modified


class PaymentDetails(XmlObject):
    """
    The payment details in the status reply
    """
    xml_name = 'paymentdetails'
    xml_fields = (
        'accountid',
        'accountholdername',
        'externaltransactionid',
    )

    def __init__(self, accountid, accountholdername, externaltransactionid):
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


class Price(Decimal):
    """
    A decimal value with currency attached.
    """

    def __new__(cls, value, currency=None):
        self = Decimal.__new__(cls, value)
        self.currency = currency
        return self

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        return cls(xml.text, xml.attrib['currency'])
