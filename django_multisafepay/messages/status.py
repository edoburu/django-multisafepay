# coding=utf-8
from django_multisafepay.data import CustomerDelivery, Transaction, Merchant
from django_multisafepay.data.status import Ewallet, PaymentDetails, StatusCustomer, CheckoutData
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

    # <status result="ok">
    #   <ewallet>
    #     <id>2118132</id>
    #     <status>completed</status>
    #     <fastcheckout>YES</fastcheckout>
    #     <created>20140305191332</created>
    #     <modified>20140305191335</modified>
    #     <reasoncode/>
    #     <reason/>
    #   </ewallet>
    #   <customer>
    #     <amount>2000</amount>      <!-- NOTE these 3 extra fields!! -->
    #     <currency>EUR</currency>
    #     <account/>
    #     <locale>en_US</locale>
    #     <firstname>Diederik</firstname>
    #     <lastname>van der Boor</lastname>
    #     <address1>Foo</address1>
    #     <address2/>
    #     <housenumber>...</housenumber>
    #     <zipcode>...</zipcode>
    #     <city>...</city>
    #     <state/>
    #     <country>NL</country>
    #     <countryname/>
    #     <phone1/>
    #     <phone2/>
    #     <email>foo@example.org</email>
    #   </customer>
    #   <customer-delivery/>
    #   <transaction>
    #     <id>7</id>
    #     <currency>EUR</currency>
    #     <amount>2000</amount>
    #     <description>...</description>
    #     <var1>5</var1>
    #     <var2/>
    #     <var3/>
    #     <items/>
    #   </transaction>
    #   <paymentdetails>
    #     <type>IDEAL</type>
    #     <accountiban>NL53INGB0654422370</accountiban>     <!--  NOTE these 3 extra fields!! -->
    #     <accountbic>INGBNL2A</accountbic>
    #     <accountid>654422370</accountid>
    #     <accountholdername>Hr E G H Küppers en/of MW M.J. Küppers-Veeneman</accountholdername>
    #     <externaltransactionid>0050000081927015</externaltransactionid>
    #   </paymentdetails>
    #   <checkoutdata version="0.1">
    #     <checkout-flow-support><merchant-checkout-flow-support>
    #       <shipping-methods>
    #         <pickup name="Online">
    #           <price currency="EUR">0.00</price>
    #         </pickup>
    #       </shipping-methods>
    #     </merchant-checkout-flow-support></checkout-flow-support>
    #     <order-adjustment>
    #       <shipping>
    #         <pickup>
    #           <shipping-name>Online</shipping-name>           <!--  NOTE different tag format!! -->
    #           <shipping-cost currency="EUR">0.00</shipping-cost>
    #         </pickup>
    #       </shipping>
    #       <adjustment-total currency="EUR">0.00</adjustment-total>
    #       <total-tax currency="EUR">0.00</total-tax>
    #     </order-adjustment>
    #     <order-total currency="EUR">20.00</order-total>
    #   </checkoutdata>
    # </status>


    def __init__(self, ewallet, customer, customer_delivery, transaction, payment_details, checkoutdata):
        """
        :type ewallet: Ewallet
        :type customer: StatusCustomer
        :type customer_delivery: CustomerDelivery
        :type transaction: Transaction
        :type payment_details: PaymentDetails
        :type checkoutdata: CheckoutData
        """
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
            customer=StatusCustomer.from_xml(xml.find('customer')),
            customer_delivery=CustomerDelivery.from_xml(xml.find('customer-delivery')),
            transaction=Transaction.from_xml(xml.find('transaction')),
            payment_details=PaymentDetails.from_xml(xml.find('paymentdetails')),
            checkoutdata=CheckoutData.from_xml(xml.find('checkoutdata'))
        )

    @property
    def status_code(self):
        return self.ewallet.status
