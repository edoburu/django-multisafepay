from django.utils.translation import to_locale

from .base import XmlObject


class GatewayCustomer(XmlObject):
    """
    Customer information, for the Gateways request
    """
    xml_name = 'customer'
    xml_fields = (
        'locale',
        'country',
    )

    def __init__(self, locale, country):
        """
        :param locale: Language code, e.g. en_US
        :param country: The 2-digit country code, in ISO 3166
        """
        self.locale = to_locale(locale)  # ensure xx_XX format
        self.country = country


class Gateway(XmlObject):
    """
    <gateway>
        <id>IDEAL</id>
        <description>iDEAL</description>
    </gateway>
    """
    xml_name = 'gateway'
    xml_fields = (
        'id',
        'description',
    )
