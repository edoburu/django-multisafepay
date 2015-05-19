from .base import MessageObject
from django_multisafepay.data.gateway import Gateway


class Gateways(MessageObject):
    """
    The message to start a checkout
    """
    xml_name = 'gateways'
    xml_fields = (
        'merchant',
        'customer',
    )

    def __init__(self, merchant, customer):
        """
        :type merchant: Merchant
        :type customer: GatewayCustomer
        """
        self.merchant = merchant
        self.customer = customer


class GatewaysReply(object):
    """
    Reply from a start_transaction call.
    """
    def __init__(self, gateways):
        """
        :param id: ID of the session
        :param payment_url: The URL to redirect to.
        """
        self.gateways = list(gateways)

    def __iter__(self):
        return iter(self.gateways)

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        gateways = xml.find('gateways')
        return cls(
            gateways=[Gateway.from_xml(gateway) for gateway in gateways]
        )
