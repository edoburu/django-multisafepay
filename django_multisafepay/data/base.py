from decimal import Decimal
from xml.sax.saxutils import escape

from django.utils.encoding import force_text

__all__ = (
    'XmlObject',
    'Price',
    'escape',
)


class XmlObject(object):
    """
    Simple object to quickly generate XML messages.
    This provides all the flexibility we need to render any XML object.
    """
    xml_name = None
    xml_attrs = None
    xml_fields = ()

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.to_xml().encode('utf-8'))

    def to_xml(self):
        # get xml message
        lines = self.get_xml_children()
        attrs = self.get_xml_attrs()
        if attrs:
            attrs = u"".join(u' {0}="{1}"'.format(k, escape(force_text(v))) for k, v in attrs.iteritems())
            return u'<{0}{1}>{2}</{0}>'.format(self.xml_name, attrs, u''.join(lines))
        else:
            return u'<{0}>{1}</{0}>'.format(self.xml_name, u''.join(lines))

    def get_xml_attrs(self):
        return self.xml_attrs

    def get_xml_children(self):
        # Allow to be overwritten
        lines = []
        for field in self.xml_fields:
            value = getattr(self, field.replace('-', '_'))
            if value is not None:
                if isinstance(value, XmlObject):
                    # Attribute name is ignored, tag name is used instead.
                    lines.append(u"{0}\n".format(value.to_xml()))
                elif isinstance(value, Price):
                    # Inconsistent API. Using decimal notation here, but using cents somewhere else.
                    lines.append(u'<{0} currency="{1}">{2:.2f}</{0}>'.format(field, value.currency, value))
                else:
                    if isinstance(value, (list, tuple)):
                        tag_value = u'\n'.join(item.to_xml() for item in value)
                    elif isinstance(value, bool):
                        tag_value = str(value).lower()
                    else:
                        tag_value = escape(force_text(value))
                    lines.append(u'<{0}>{1}</{0}>'.format(field, tag_value))
        return lines

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        if xml is None:
            return None
        kwargs = cls.get_class_kwargs(xml)  # Make kwargs available in debugging stack frame.
        return cls(**kwargs)

    @classmethod
    def get_class_kwargs(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        kwargs = {}
        for field in cls.xml_fields:
            node = xml.find(field)
            kwargs[field.replace('-', '_')] = None if node is None else node.text
        return kwargs


class Price(Decimal):
    """
    A decimal value with currency attached.
    """

    def __new__(cls, value, currency=None):
        self = Decimal.__new__(cls, value)
        self.currency = currency
        return self

    @classmethod
    def from_xml(cls, xml):
        """
        :type xml: xml.etree.ElementTree.Element
        """
        return cls(xml.text, xml.attrib['currency'])
