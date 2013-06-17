from zope import component
from zope import interface
from zope import schema
from z3c.form import field

#from plone.autoform import directives as form
from plone.app.collection import _ as _c
from plone.app.portlets.portlets import base
from plone.app.portlets.browser import z3cformhelper
#from plone.formwidget.querystring.widget import QueryStringFieldWidget
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.favoriting import FavoritingPortletMessageFactory as _
from collective.favoriting.browser.favoriting_view import VIEW_NAME
from plone.app.layout.viewlets.common import ViewletBase


class IFavoritingPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    title = schema.TextLine(title=_(u"Title"), required=False)

#    form.widget(query=QueryStringFieldWidget)
#    query = schema.List(
#        title=_c(u'Search terms'),
#        value_type=schema.Dict(value_type=schema.Field(),
#                               key_type=schema.TextLine()),
#        required=False
#    )

    sort_on = schema.TextLine(
        title=_c(u'label_sort_on', default=u'Sort on'),
        description=_c(u"Sort the collection on this index"),
        required=False,
    )

    sort_reversed = schema.Bool(
        title=_c(u'label_sort_reversed', default=u'Reversed order'),
        description=_c(u'Sort the results in reversed order'),
        required=False,
    )

    limit = schema.Int(
        title=_c(u'label_limit', default=u'Limit'),
        description=_c(u'Limit Search Results'),
        required=False,
        default=1000,
    )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    interface.implements(IFavoritingPortlet)

    title = None
    query = None
    sort_on = None
    sort_reversed = None
    limit = None

    def __init__(
        self,
        title=None,
        #query=None,
        sort_on=None,
        sort_reversed=None,
        limit=None,
    ):
        self._title = title
#        self.query = query
        self.query = None
        self.sort_on = sort_on
        self.sort_reversed = sort_reversed
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
        #query.update(self.data.get(query))
        limit = self.data.get("limit", None)
        sort_on = self.data.get("sort_on", None)
        sort_reversed = self.data.get("sort_reversed")
        if limit is not None:
            query["sort_on"] = "effective"
            query["sort_reversed"] = True
            query["limit"] = limit
        if sort_on is not None:
            query["sort_on"] = sort_on
        if sort_reversed is not None:
            query["sort_reversed"] = sort_reversed
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
