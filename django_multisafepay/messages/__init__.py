"""
The messages are mainly used for internal purposes.
The describe the XML format for the calls that the MultiSafepay client makes.
"""
from .checkouttransaction import CheckoutTransaction, CheckoutTransactionReply
from .directtransaction import DirectTransaction, DirectTransactionReply
from .status import Status, StatusReply
from .gateway import Gateways, GatewaysReply
from .redirecttransaction import RedirectTransaction, RedirectTransactionReply

__all__ = (
    'CheckoutTransaction',
    'CheckoutTransactionReply',

    'Status',
    'StatusReply',

    'Gateways',
    'GatewaysReply',

    'RedirectTransaction',
    'RedirectTransactionReply',

    'DirectTransaction',
    'DirectTransactionReply',
)
