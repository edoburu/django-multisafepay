"""
All exceptions raised by this package.
"""


class MultiSafepayException(Exception):
    """
    Base class for all exceptions from MultiSafepay
    """
    CODE_INVALID_TRANSACTION_ID = '1006'


class MultiSafepayServerException(MultiSafepayException):
    """
    Base class for reported errors via the API.
    """

    def __init__(self, code, description):
        super(MultiSafepayServerException, self).__init__("{0}: {1}".format(code, description))
        self.code = code
        self.description = description

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        error = xml.find('error')
        kwargs = dict(
            code=error.find('code').text,
            description=error.find('description').text
        )

        # NOTE: depending on the error code, some custom elements might be available.
        # This is currently not being checked for.
        # We could implement a class type per exception code, if that's needed.

        return cls(**kwargs)
