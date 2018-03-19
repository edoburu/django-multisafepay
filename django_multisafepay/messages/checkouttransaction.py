from .redirecttransaction import RedirectTransaction, RedirectTransactionReply


class CheckoutTransaction(RedirectTransaction):
    """
    The message to start a checkout, using the Fast-Connect method.
    """
    xml_name = 'checkouttransaction'
    xml_fields = (
        'merchant',
        'plugin',
        'customer',
        'customer_delivery',
        'cart',             # TODO: Cart data model not implemented yet   (uses Google Checkout Cart format)
        'fields',           # TODO: Fields data model not implemented yet (for custom form fields)
        'google_analytics',
        'checkout_settings',
        'transaction',
        'signature',
    )

    def __init__(self, merchant, transaction, customer, customer_delivery=None, cart=None, fields=None, plugin=None, checkout_settings=None, google_analytics=None):
        """
        :type merchant: Merchant
        :type transaction: Transaction
        :type customer: Customer
        :type customer_delivery: CustomerDelivery
        :type cart: Cart
        :type plugin: Plugin
        :type google_analytics: GoogleAnalytics
        """
        super(CheckoutTransaction, self).__init__(
            merchant=merchant,
            transaction=transaction,
            customer=customer,
            google_analytics=google_analytics
        )

        # Fast-Checkout fields that are not present in the redirecttransaction of the Connect method.
        self.plugin = plugin
        self.customer_delivery = customer_delivery
        self.cart = cart
        self.fields = fields
        self.checkout_settings = checkout_settings


class CheckoutTransactionReply(RedirectTransactionReply):
    """
    Reply from a start_transaction call.
    Is identical to the Connect method reply.
    """
