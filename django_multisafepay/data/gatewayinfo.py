from .base import XmlObject


class GatewayInfo(XmlObject):
    """
    <gatewayinfo>
        <issuerid>0151</issuerid>
    </gatewayinfo>
    """
    xml_name = 'gatewayinfo'
    xml_fields = (
        'issuerid',
    )

    def __init__(self, issuerid):
        self.issuerid = issuerid
