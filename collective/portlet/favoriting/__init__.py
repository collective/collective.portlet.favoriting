from zope.i18nmessageid import MessageFactory
FavoritingPortletMessageFactory = MessageFactory('collective.portlet.favoriting')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
