from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.Archetypes.ArchetypeTool import registerType
from Products.CMFCore import permissions
from Products.Five.browser import BrowserView
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.config import PROJECTNAME
from bika.lims import bikaMessageFactory as _
from bika.lims.interfaces import ISamplePoints
from bika.lims.content.bikaschema import BikaFolderSchema
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.folder.folder import ATFolder, ATFolderSchema
from zope.interface.declarations import implements
from Products.CMFCore.utils import getToolByName
import json

class SamplePointsView(BikaListingView):
    implements(IFolderContentsView)

    def __init__(self, context, request):
        super(SamplePointsView, self).__init__(context, request)
        self.contentFilter = {'portal_type': 'SamplePoint',
                              'sort_on': 'sortable_title'}
        self.content_add_actions = {_('Sample Point'):
                                    "createObject?type_name=SamplePoint"}
        self.title = _("Sample Points")
        self.description = ""
        self.show_editable_border = False
        self.show_filters = True
        self.show_sort_column = False
        self.show_select_row = True
        self.show_select_column = True
        self.pagesize = 20

        self.columns = {
            'Title': {'title': _('Sample Point')},
                   'Description': {'title': _('Description')},
        }
        self.review_states = [
            {'title': _('All'), 'id':'all',
             'columns': ['Title', 'Description']}
        ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj'].getObject()
            items[x]['Description'] = obj.Description()
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                 (items[x]['url'], items[x]['Title'])


        return items

schema = ATFolderSchema.copy()

class SamplePoints(ATFolder):
    implements(ISamplePoints)
    schema = schema
    displayContentsTab = False
schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(SamplePoints, PROJECTNAME)

class AJAX_SamplePoints():
    """ autocomplete data source for sample points field
        return JSON data [string,string]
    """
    def __call__(self):
        pc = getToolByName(self, 'portal_catalog')
        term = self.request.get('term', '')
        items = pc(portal_type = "SamplePoint")
        nr_items = len(items)
        items = [s.Title for s in items if s.Title.lower().find(term.lower()) > -1]
        return json.dumps(items)

