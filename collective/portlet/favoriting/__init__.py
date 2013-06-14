from zope.i18nmessageid import MessageFactory
mfid = 'collective.portlet.favoriting'
FavoritingPortletMessageFactory = MessageFactory(mfid)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
