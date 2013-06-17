from zope.interface import implements
from zope import schema

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper

from z3c.form import field

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.favoriting import FavoritingPortletMessageFactory as _


class IFavoritingPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    title = schema.TextLine(title=_(u"Title"), required=False)
    limit = schema.Int(title=_(u"Limit"), required=False)
    ftype = schema.Choice(
        title=_(u"Filter by type"),
        required=False,
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
    )

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IFavoritingPortlet)

    title = None
    limit = None
    ftype = None

    def __init__(self, title=None, limit=None, ftype=None):
        self._title = title
        self.limit = limit
        self.ftype = ftype

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self._title is None:
            return _(u"Favorites")
        return self._title


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('favoritingportlet.pt')


class AddForm(z3cformhelper.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = field.Fields(IFavoritingPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = field.Fields(IFavoritingPortlet)
