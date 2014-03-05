django-multisafepay
===================

Payment gateway integration for `MultiSafepay <https://www.multisafepay.com/>`_.
MultiSafepay is a large payment gateway based in The Netherlands that supports many international payment methods.

MultiSafepay offers two methods for payments, see https://www.multisafepay.com/en/Payment-services/:

* `Fast checkout <https://www.multisafepay.com/en/fast-checkout/>`_ (requires customer login)
* `Connect <https://www.multisafepay.com/en/connect/>`_ (full form input on your site)

This package currently only implements the methods for the fast checkout method.
Contributions to support the Connect method are welcome!


Installation
============

Install via pip::

    pip install django-multisafepay


Configuration
-------------

In the MultiSafepay merchant `site settings <https://merchant.multisafepay.com/account/details/sites/>`_,
add a new website. Use those settings to configure the application:

`MULTISAFEPAY_ACCOUNT_ID`
    The account ID, provided by MultiSafepay.

`MULTISAFEPAY_SITE_ID`
    The site ID, found in the MultiSafepay website settings panel.

`MULTISAFEPAY_SITE_CODE`
    The site security code, found in the MultiSafepay website settings panel.

`MULTISAFEPAY_TESTING`
    Whether or not to run in testing mode. Defaults to `True`.

Add to ``urls.py``::

    urlpatterns += patterns('',
        url(r'^api/multisafepay/', include('django_multisafepay.urls')),
    )

As recommendation, temporary log all events from this package as well::

    LOGGING = {
        # ...

        'handlers': {
            # ...

            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            # ...

            'django_multisafepay': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }


Usage
=====

Creating a new payment transaction::

    from django_multisafepay.client import MultiSafepayClient
    from django_multisafepay.data import Transaction, Customer
    from django.shortcuts import redirect

    def pay(request):

        client = MultiSafepayClient()
        reply = client.start_checkout(
            transaction = Transaction(

            ),
            customer = Customer(

            )
        )

        return redirect(reply.payment_url)


Fetching status::

    client = MultiSafepayClient()
    statusreply = client.status(self.transaction_id)


TODO
====

* Integrate nicely in django-merchant_ or django-getpaid_.
* Not all XML features are implemented, e.g.:

 * checkout-shopping-cart
 * custom-fields
 * shipping



.. _django-merchant: https://github.com/agiliq/merchant
.. _django-getpaid: https://github.com/cypreess/django-getpaid
