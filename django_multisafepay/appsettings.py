"""
Settings for this application
"""
from django.conf import settings

MULTISAFEPAY_ACCOUNT_ID = getattr(settings, 'MULTISAFEPAY_ACCOUNT_ID')
MULTISAFEPAY_SITE_ID = getattr(settings, 'MULTISAFEPAY_SITE_ID')
MULTISAFEPAY_SITE_CODE = getattr(settings, 'MULTISAFEPAY_SITE_CODE')

# Whether to use the testing mode, or live mode.
MULTISAFEPAY_TESTING = getattr(settings, 'MULTISAFEPAY_TESTING', True)

# Allow to define the URLs globally (e.g. using reverse_lazy())
MULTISAFEPAY_REDIRECT_URL = getattr(settings, 'MULTISAFEPAY_REDIRECT_URL', None)
MULTISAFEPAY_CANCEL_URL = getattr(settings, 'MULTISAFEPAY_CANCEL_URL', None)
