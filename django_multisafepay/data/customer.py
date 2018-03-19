from .base import XmlObject


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

    def __init__(self, locale, firstname, lastname, address1, address2, housenumber, zipcode, city, state, country, phone, email, ipaddress=None, forwardedip=None, referrer=None, user_agent=None):
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

    @classmethod
    def from_customer(cls, customer):
        """
        Initialize this class using the information of the customer.
        """
        return cls(
            firstname=customer.firstname,
            lastname=customer.lastname,
            address1=customer.address1,
            address2=customer.address2,
            housenumber=customer.housenumber,
            zipcode=customer.zipcode,
            city=customer.city,
            state=customer.state,
            country=customer.country,
            phone=customer.phone,
            email=customer.email,
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
