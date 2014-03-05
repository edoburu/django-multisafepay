from django_multisafepay import USER_AGENT
from django_multisafepay.data.base import XmlObject


class MessageObject(XmlObject):
    """
    A root XML node.
    """
    def to_xml(self):
        lines = self.get_xml_children()
        return u'<?xml version="1.0" encoding="UTF-8"?>\n' \
               u'<{0} ua="{1}">{2}</{0}>'.format(self.xml_name, USER_AGENT, u''.join(lines))
