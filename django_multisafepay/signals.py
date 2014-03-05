from django.dispatch import Signal

# The signal which is fired when the notification URL is called.
order_status_updated = Signal(providing_args=["statusreply", "request"])
