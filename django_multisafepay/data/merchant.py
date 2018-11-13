from django_multisafepay import PLUGIN_VERSION, SHOP_NAME, appsettings

from .base import XmlObject

try:
    from django.urls import reverse
except ImportError:  # Django < 1.10
    from django.core.urlresolvers import reverse


class Merchant(XmlObject):
    """
    Meta information for the webshop.
    """
    xml_name = 'merchant'
    xml_fields = (
        'account',
        'site_id',
        'site_secure_code',
        'notification_url',
        'cancel_url',
        'redirect_url',
        'close_window',
    )

    def __init__(self, account=None, site_id=None, site_code=None, notification_url=None, cancel_url=None, redirect_url=None, close_window=None):
        """
        If the account, site_id and site_code are omitted, the defaults are read from the settings file.
        """
        self.account = account or appsettings.MULTISAFEPAY_ACCOUNT_ID
        self.site_id = site_id or appsettings.MULTISAFEPAY_SITE_ID
        self.site_secure_code = site_code or appsettings.MULTISAFEPAY_SITE_CODE

        # Custom configuration
        self.notification_url = notification_url or reverse('notification_url')
        self.cancel_url = cancel_url or appsettings.MULTISAFEPAY_CANCEL_URL
        self.redirect_url = redirect_url or appsettings.MULTISAFEPAY_REDIRECT_URL
        self.close_window = close_window


class Plugin(XmlObject):
    """
    Meta information for the plugin
    """
    xml_name = 'plugin'
    xml_fields = (
        'shop',
        'shop_version',
        'plugin_version',
        'partner',
        'shop_root_url',
    )

    def __init__(self, shop=None, shop_version=None, plugin_version=None, partner=None, shop_root_url=None):
        """
        :param shop: Name of the webshop software (defaults to "django-multisafepay")
        :param shop_version: Version of the webshop software.
        :param plugin_version: Version of this plugin (defaults to current package version)
        """
        self.shop = shop or SHOP_NAME
        self.shop_version = shop_version
        self.plugin_version = plugin_version or PLUGIN_VERSION
        self.partner = partner
        self.shop_root_url = shop_root_url
