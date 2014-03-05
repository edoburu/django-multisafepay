from .base import XmlObject, escape


class Cart(XmlObject):
    """
    The shopping cart.
    """
    xml_name = 'checkout-shopping-cart'

    def __init__(self, items=(), shipping_methods=(), tax_tables=()):
        """
        :type items: list of :class:`Item`
        """
        self.items = list(items or ())
        self.shipping_methods = list(shipping_methods or ())
        self.tax_tables = list(tax_tables or ())

    def get_xml_children(self):
        lines = []
        if self.items:
            # Don't bother creating sub elements for the shopping cart, make this object smarter.
            lines.append('<shopping-cart><items>\n')
            for item in self.items:
                lines.append("  {0}\n".format(item.to_xml()))
            lines.append('</items></shopping-cart>\n')

        if self.shipping_methods or self.tax_tables:
            lines.append('<checkout-flow-support><merchant-checkout-flow-support>\n')

            if self.shipping_methods:
                lines.append('<shipping-methods>\n')
                for item in self.shipping_methods:
                    lines.append("  {0}\n".format(item.to_xml()))
                lines.append('</shipping-methods>\n')

            if self.tax_tables:
                lines.append('<tax-tables>\n')
                for item in self.tax_tables:
                    lines.append("  {0}\n".format(item.to_xml()))
                lines.append('</tax-tables>\n')

            lines.append('</merchant-checkout-flow-support></checkout-flow-support>\n')
        return lines


class ShoppingCartItem(XmlObject):
    """
    An item in the shopping cart.
    """
    xml_name = 'item'
    xml_fields = (
        'item-name',
        'item-description',
        'unit-price',
        'quantity',
        'merchant-item-id'
        'item-weight'  # unit="KG" value="1"
    )

    def __init__(self, item_name, item_description, unit_price, quantity, merchant_item_id, item_weight=None):
        """
        :type unit_price: Price
        :type item_weight: ItemWeight
        """
        self.item_name = item_name
        self.item_description = item_description
        self.unit_price = unit_price
        self.quantity = quantity
        self.merchant_item_id = merchant_item_id
        self.item_weight = item_weight


class ItemWeight(XmlObject):
    """
    Weight value for an item in the shopping cart.
    """
    xml_name = 'item-weight'

    def __init__(self, value, unit):
        """
        :param value: The actual value.
        :param unit: The units, e.g. "KG".
        """
        self.value = value
        self.unit = unit

    def to_xml(self):
        return u'<{0} unit="{1}" value="{2}" />'.format(self.xml_name, escape(self.unit), escape(str(self.value)))


class ShippingMethodBase(XmlObject):
    """
    Base class for shipping methods
    """
    xml_fields = (
        'price',
    )

    def __init__(self, name, price):
        """
        :type name: str
        :type price: Price
        """
        self.name = name
        self.price = price

    def get_xml_attrs(self):
        return {
            'name': self.name
        }


class Pickup(ShippingMethodBase):
    """
    Shipping costs for pickup.
    """
    xml_name = 'pickup'


class FlatRateShipping(ShippingMethodBase):
    """
    Shipping costs for flat-rates
    """
    xml_name = 'flat-rate-shipping'
    xml_fields = ShippingMethodBase.xml_fields + (
        'shipping_restrictions',  # TODO: data class is not implemented.
    )

    def __init__(self, name, price, restrictions=None):
        """
        :type name: str
        :type price: Price
        :type restrictions
        :param restrictions: Not implemented yet.
        """
        super(FlatRateShipping, self).__init__(name, price)
        self.restrictions = restrictions
