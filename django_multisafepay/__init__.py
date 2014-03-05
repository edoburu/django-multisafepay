import django

# following PEP 386
__version__ = "0.1"

SHOP_NAME = "django-multisafepay"
PLUGIN_VERSION = __version__

USER_AGENT = '{0}/{1} (Django {2}.{3}.x)'.format(SHOP_NAME, PLUGIN_VERSION, django.VERSION[0], django.VERSION[1])
