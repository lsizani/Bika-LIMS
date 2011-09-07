from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.Archetypes.ArchetypeTool import registerType
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.config import PROJECTNAME
from bika.lims import bikaMessageFactory as _
from bika.lims.content.bikaschema import BikaFolderSchema
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.folder.folder import ATFolder, ATFolderSchema
from bika.lims.interfaces import IARProfiles
from zope.interface.declarations import implements

class ARProfilesView(BikaListingView):
    implements(IFolderContentsView)

    def __init__(self, context, request):
        super(ARProfilesView, self).__init__(context, request)
        self.contentFilter = {'portal_type': 'ARProfile',
                              'sort_on': 'sortable_title'}
        self.content_add_actions = {_('AR Profile'):
                                    "createObject?type_name=ARProfile"}
        self.title = _("Analysis Request Profiles")
        self.description = ""
        self.show_editable_border = False
        self.show_filters = False
        self.show_sort_column = False
        self.show_select_row = True
        self.show_select_column = True
        self.pagesize = 20

        self.columns = {
            'title': {'title': _('Profile')},
            'Description': {'title': _('Description')},
            'getProfileKey': {'title': _('Profile Key')},
        }
        self.review_states = [
            {'title': _('All'), 'id':'all',
             'columns': ['title', 'Description', 'getProfileKey'],
             }
        ]

    @property
    def folderitems(self):
        items = BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            items[x]['replace']['title'] = "<a href='%s'>%s</a>" % \
                 (items[x]['url'], items[x]['title'])

        return items

schema = ATFolderSchema.copy()
class ARProfiles(ATFolder):
    implements(IARProfiles)
    schema = schema
    displayContentsTab = False
schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(ARProfiles, PROJECTNAME)
