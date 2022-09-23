django-multisafepay
===================

Payment gateway integration for `MultiSafepay <https://www.multisafepay.com/>`_.
MultiSafepay is a Dutch payment services provider that supports many international payment methods.

This SDK supports:

- [FastCheckout](https://docs.multisafepay.com/docs/fastcheckout)
- [Payment pages](https://docs.multisafepay.com/docs/payment-pages)


Installation
============

To install via pip::

    pip install django-multisafepay


Configuration
-------------

1. Sign in to your `MultiSafepay dashboard <https://merchant.multisafepay.com/>`_.
2. Go to **Integrations** > **Sites**, and then click **Add new site**. 
3. Enter the required information about your site. 
4. From the **Site profile** page, copy the following details:

`MULTISAFEPAY_ACCOUNT_ID`

`MULTISAFEPAY_SITE_ID`

`MULTISAFEPAY_SITE_CODE` 
    The site security code.

`MULTISAFEPAY_TESTING`
    Whether or not to run in testing mode. Defaults to `True`.

5. To configure the application, add to ``urls.py``::

    urlpatterns += patterns('',
        url(r'^api/multisafepay/', include('django_multisafepay.urls')),
    )

6. We recommend temporarily logging all events from this package::

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

To create a new order::

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


- For FastCheckout orders, use the ``start_checkout()`` method.
- For payment page orders, use the ``redirect_transaction()`` method.

Both methods return an URL to redirect the customer to.

Fetching status::

    client = MultiSafepayClient()
    statusreply = client.status(self.transaction_id)


TODO
====

- Integrate cleanly in django-merchant_ or django-getpaid_.
- Not all XML features are implemented, e.g.:

 * checkout-shopping-cart
 * custom-fields
 * shipping
 * iDEAL issuers request (simple to add)



.. _django-merchant: https://github.com/agiliq/merchant
.. _django-getpaid: https://github.com/cypreess/django-getpaid
