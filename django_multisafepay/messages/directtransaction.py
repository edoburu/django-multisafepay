from .redirecttransaction import RedirectTransaction, RedirectTransactionReply


class DirectTransaction(RedirectTransaction):
    """
    The message to start a checkout and skip the initial choices, using the Fast-Connect method.
    """
    xml_name = 'directtransaction'
    xml_fields = RedirectTransaction.xml_fields + (
        'gatewayinfo',
    )

    def __init__(self, merchant, transaction, customer, gatewayinfo, google_analytics=None):
        """
        :type merchant: Merchant
        :type transaction: Transaction
        :type customer: Customer
        :type gatewayinfo: GatewayInfo
        :type google_analytics: GoogleAnalytics
        """
        super(DirectTransaction, self).__init__(
            merchant=merchant,
            transaction=transaction,
            customer=customer,
            google_analytics=google_analytics
        )

        self.gatewayinfo = gatewayinfo


class DirectTransactionReply(RedirectTransactionReply):
    """
    Reply from a directtransaction call.
    Is identical to the standard method reply.
    """
