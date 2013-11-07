from zope import component
from zope import interface
from zope import schema
from z3c.form import field

#from plone.autoform import directives as form
from Products.CMFPlone import PloneMessageFactory as _p
from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper
#from plone.formwidget.querystring.widget import QueryStringFieldWidget
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.favoriting import FavoritingPortletMessageFactory as _
from collective.favoriting.browser.favoriting_view import VIEW_NAME


class IFavoritingPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    title = schema.TextLine(title=_p(u"Title"), required=False)

    portal_type = schema.Choice(
        title=_p(u"Content Type"),
        required=False,
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"
    )

    limit = schema.Int(
        title=_p(u'label_limit', default=u'Limit'),
        description=_p(u'Limit Search Results'),
        required=False,
        default=100,
    )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    interface.implements(IFavoritingPortlet)

    title = None
    limit = None
    portal_type = None

    def __init__(self, title=None, portal_type=None, limit=None):
        self._title = title
        self.portal_type = portal_type
        self.limit = limit

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

    def get_favorites(self):
        manager = self.context.restrictedTraverse(VIEW_NAME)
        query = {}
        query["sort_on"] = "sortable_title"
        limit = self.data.get("limit", None)
        if limit is not None:
            query["limit"] = limit
        portal_type = self.data.get("portal_type", None)
        if portal_type is not None:
            query["portal_type"] = portal_type
        return manager.get(query=query)

    def site_url(self):
        portal_state = component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        return portal_state.portal_url()


class AddForm(z3cformhelper.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    fields = field.Fields(IFavoritingPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    fields = field.Fields(IFavoritingPortlet)
