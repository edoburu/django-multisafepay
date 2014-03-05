"""
The data objects can be provided as parameters to the client.
"""
from xml.sax.saxutils import escape
from decimal import Decimal
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django_multisafepay import appsettings, SHOP_NAME, PLUGIN_VERSION


