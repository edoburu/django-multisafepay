# coding=utf-8
from django_multisafepay.data import CustomerDelivery, Merchant, Transaction
from django_multisafepay.data.status import CheckoutData, CustomerStatus, Ewallet, PaymentDetails, TransactionStatus

from .base import XmlRequest, XmlResponse


class Status(XmlRequest):
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
            account=merchant.account,
            site_id=merchant.site_id,
            site_code=merchant.site_secure_code,
        )
        self.transaction = Transaction(id=transaction_id)


class StatusReply(XmlResponse):
    """
    Reply from a status call.
    """

    # Fast Checkout example:
    # -----------------------
    #
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
    #     <accountiban>NL30INGB0123456789</accountiban>     <!--  NOTE these 3 extra fields because of iDEAL!! -->
    #     <accountbic>INGBNL2A</accountbic>
    #     <accountid>654412345</accountid>
    #     <accountholdername>Mr Küppers</accountholdername>
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
    #
    #
    # Connect example:
    # ------------------
    #
    # <status result="ok">
    #   <ewallet>
    #     <id>50102723</id>
    #     <status>completed</status>
    #     <fastcheckout>NO</fastcheckout>
    #     <created>20150526130908</created>
    #     <modified>20150526131108</modified>
    #     <reasoncode />
    #     <reason />
    #   </ewallet>
    #   <customer>
    #     <amount>6000</amount>
    #     <currency>EUR</currency>
    #     <account />
    #     <locale>nl_NL</locale>
    #     <firstname>Diederik</firstname>
    #     <lastname>van der Boor</lastname>
    #     <address1>Foo</address1>
    #     <address2 />
    #     <housenumber>...</housenumber>
    #     <zipcode>...</zipcode>
    #     <city>...</city>
    #     <state />
    #     <country>FR</country>
    #     <countryname />
    #     <phone1>+33 123456789</phone1>
    #     <phone2 />
    #     <email>foo@example.org</email>
    #   </customer>
    #   <customer-delivery />
    #   <transaction>
    #     <id>10217</id>
    #     <recurringid />
    #     <currency>EUR</currency>
    #     <amount>6000</amount>
    #     <cost>174</cost>
    #     <description>...</description>
    #     <var1>215</var1>
    #     <var2 />
    #     <var3 />
    #     <items />
    #     <amountrefunded>0</amountrefunded>
    #   </transaction>
    #   <paymentdetails>
    #     <type>MASTERCARD</type>
    #     <accountid />
    #     <accountholdername>A.B. Tester/accountholdername>
    #     <externaltransactionid>2-70-370907</externaltransactionid>
    #   </paymentdetails>
    # </status>

    def __init__(self, ewallet, customer, customer_delivery, transaction, payment_details, checkoutdata=None):
        """
        :type ewallet: Ewallet
        :type customer: CustomerStatus
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

    STATUS_INITIALIZED = "initialized"  # waiting
    STATUS_COMPLETED = "completed"     # payment complete
    STATUS_WAITING = "uncleared"       # waiting (credit cards or direct debit)
    STATUS_CANCELLED = "void"          # canceled
    STATUS_DECLINED = "declined"       # declined
    STATUS_REFUNDED = "refunded"       # refunded
    STATUS_EXPIRED = "expired"         # expired

    @classmethod
    def get_class_kwargs(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        return dict(
            ewallet=Ewallet.from_xml(xml.find('ewallet')),
            customer=CustomerStatus.from_xml(xml.find('customer')),
            customer_delivery=CustomerDelivery.from_xml(xml.find('customer-delivery')),
            transaction=TransactionStatus.from_xml(xml.find('transaction')),
            payment_details=PaymentDetails.from_xml(xml.find('paymentdetails')),
            checkoutdata=CheckoutData.from_xml(xml.find('checkoutdata')),
        )

    @property
    def status_code(self):
        return self.ewallet.status
