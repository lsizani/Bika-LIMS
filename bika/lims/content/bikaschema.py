from Products.Archetypes.public import BaseSchema
from plone.app.folder.folder import ATFolder, ATFolderSchema

BikaSchema = BaseSchema.copy()
BikaSchema['id'].widget.visible = False
BikaSchema['description'].widget.visible = False
BikaSchema['description'].schemata = 'default'
BikaSchema['allowDiscussion'].widget.visible = False
BikaSchema['creators'].widget.visible = False
BikaSchema['contributors'].widget.visible = False
BikaSchema['rights'].widget.visible = False
BikaSchema['effectiveDate'].widget.visible = False
BikaSchema['expirationDate'].widget.visible = False
BikaSchema['subject'].widget.visible = False
BikaSchema['language'].widget.visible = False
BikaSchema['location'].widget.visible = False

BikaFolderSchema = ATFolderSchema.copy()
BikaFolderSchema['excludeFromNav'].widget.visible = False
BikaFolderSchema['nextPreviousEnabled'].widget.visible = False
BikaFolderSchema['id'].widget.visible = False
BikaFolderSchema['description'].widget.visible = False
BikaFolderSchema['allowDiscussion'].widget.visible = False
BikaFolderSchema['creators'].widget.visible = False
BikaFolderSchema['contributors'].widget.visible = False
BikaFolderSchema['rights'].widget.visible = False
BikaFolderSchema['effectiveDate'].widget.visible = False
BikaFolderSchema['expirationDate'].widget.visible = False
BikaFolderSchema['subject'].widget.visible = False
BikaFolderSchema['language'].widget.visible = False
BikaFolderSchema['location'].widget.visible = False
