from xml.etree import ElementTree

from django_multisafepay import USER_AGENT
from django_multisafepay.data.base import XmlObject


class XmlRequest(XmlObject):
    """
    A root XML node.
    """

    def to_xml(self):
        lines = self.get_xml_children()
        return u'<?xml version="1.0" encoding="UTF-8"?>\n' \
               u'<{0} ua="{1}">{2}</{0}>'.format(self.xml_name, USER_AGENT, u''.join(lines))


class XmlResponse(object):
    """
    Base class for response objects.
    """
    _xml = None

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        if xml is None:
            return None
        kwargs = cls.get_class_kwargs(xml)  # Make kwargs available in debugging stack frame.
        reply = cls(**kwargs)
        reply._xml = xml  # Inject response for better logging in Sentry.
        return reply

    @classmethod
    def get_class_kwargs(cls, xml):
        """
        Custom method to override, provide all ``__init__()`` fields by parsing the XML.
        :param xml: The incoming XML message
        :type xml: xml.etree.ElementTree.Element
        :return: The parameters for the init method.
        :rtype: dict
        """
        return {}

    def __repr__(self):
        if self._xml is not None:
            return '<{0} {1}>'.format(self.__class__.__name__, ElementTree.tostring(self._xml, encoding='utf8'))
        else:
            return '<{0} without _xml data>'.format(self.__class__.__name__)
