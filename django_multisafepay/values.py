"""
The data objects can be provided as parameters to the client.
"""
from decimal import Decimal
from xml.sax.saxutils import escape

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django_multisafepay import PLUGIN_VERSION, SHOP_NAME, appsettings
