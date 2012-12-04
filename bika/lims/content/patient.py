from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import manage_users
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.utils import DT2dt
from Products.ATExtensions.ateapi import RecordsField
from Products.Archetypes import atapi
from Products.Archetypes.public import *
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from bika.lims import PMF, bikaMessageFactory as _
from bika.lims.browser.fields import AddressField
from bika.lims.browser.widgets import AddressWidget
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.browser.widgets import PatientIdentifiersWidget
from bika.lims.browser.widgets import ReadonlyStringWidget
from bika.lims.browser.widgets import RecordsWidget
from bika.lims.browser.widgets import SplittedDateWidget
from bika.lims.config import ManageClients, PUBLICATION_PREFS, PROJECTNAME, \
    GENDERS, ETHNICITIES
from bika.lims.content.person import Person
from bika.lims.interfaces import IPatient
from bika.lims.permissions import *
from datetime import datetime
from zope.interface import implements

schema=Person.schema.copy()+Schema((
    StringField('PatientID',
        searchable=1,
        required=0,
        widget=ReadonlyStringWidget(
            visible={'view': 'visible','edit': 'hidden' },
            label=_('Patient ID'),
            css='readonly-emphasize',
        ),
    ),
    ReferenceField('PrimaryReferrer',
        vocabulary='get_clients',
        allowed_types=('Client',),
        relationship='PatientClient',
        required=1,
        widget=SelectionWidget(
            format='select',
            label=_('Primary Referrer'),
        ),
    ),
    ComputedField('PrimaryReferrerUID',
        expression='here.getPrimaryReferrer() and here.getPrimaryReferrer().UID() or None',
        widget=ComputedWidget(
        ),
    ),
    StringField('Gender',
        vocabulary=GENDERS,
        index='FieldIndex',
        widget=SelectionWidget(
            format='select',
            label=_('Gender'),
        ),
    ),
    StringField('Age',
        widget=StringWidget(
            label=_('Age'),
            visible=1,
            width=3,
        ),
    ),
    DateTimeField('BirthDate',
        required=1,
        widget=DateTimeWidget(
            label=_('Birth date'),
        ),
    ),
    BooleanField('BirthDateEstimated',
        default=False,
        widget=BooleanWidget(
            label=_('Birth date is estimated'),
        ),
    ),
    RecordsField('AgeSplitted',
        required=1,
        widget=SplittedDateWidget(
            label=_('Age'),
        ),
    ),
    AddressField('CountryState',
        widget = AddressWidget(
           label = _("Country and state"),
           showLegend = True,
           showDistrict = False,
           showCopyFrom = False,
           showCity =  False,
           showPostalCode = False,
           showAddress = False,
        ),
    ),
    RecordsField('PatientIdentifiers',
        type='patientidentifiers',
        subfields=('IdentifierTypeUID','IdentifierType','Identifier'),
        subfield_labels={'IdentifierType':_('Identifier Type'),'Identifier': _('Identifier')},
        subfield_sizes={'Identifier': 15,'Identifier Type': 25},
        widget=PatientIdentifiersWidget(
            label=_('Additional identifiers'),
            description=_('Patient additional identifiers')
        ),
    ),
    TextField('Remarks',
        searchable=True,
        default_content_type='text/x-web-intelligent',
        allowable_content_types=('text/x-web-intelligent',),
        default_output_type="text/html",
        widget=TextAreaWidget(
            macro="bika_widgets/remarks",
            label=_('Remarks'),
            append_only=True,
        ),
    ),
    RecordsField('TreatmentHistory',
        type='treatmenthistory',
        subfields=('Treatment','Drug','Start','End','Remarks'),
        required_subfields=('Drug','Start','End'),
        subfield_labels={'Drug': _('Drug'),'Start':_('Start'),
                         'End': _('End'),'Remarks': _('Remarks')},
        subfield_sizes={'Drug':40,'Start':10,'End':10,'Remarks':25},
        widget=RecordsWidget(
            label='Drug History',
            description=_("A list of patient treatments and drugs administered."),
            visible=False,# uses view from browser/patient.py
        ),
    ),
    RecordsField('Allergies',
        type='allergies',
        subfields=('DrugProhibition','Drug','Remarks'),
        required_subfields=('DrugProhibition','Drug'),
        subfield_labels={'DrugProhibition':_('Drug Prohibition Explanation'),'Drug': _('Drug'),
                         'Remarks': _('Remarks')},
        subfield_sizes={'DrugProhibition':20,'Drug':20,'Remarks':25},
        widget=RecordsWidget(
            label='Allergies',
            description=_("Known Patient allergies to keep information that can aid drug reaction interpretation"),
            visible=False,# uses view from browser/patient.py
        ),
    ),
    RecordsField('ImmunizationHistory',
        type='immunizationhistory',
        subfields=('EPINumber','Immunization','VaccinationCenter','Date','Remarks'),
        required_subfields=('EPINumber','Immunization','Date'),
        subfield_labels={'EPINumber':_('EPI Number'),'Immunization': _('Immunization'),
                         'VaccinationCenter':_('Vaccination Center'),'Date': _('Date'),
                         'Remarks': _('Remarks')},
        subfield_sizes={'EPINumber':12,'Immunization':20,'VaccinationCenter':10,'Date':10,'Remarks':25},
        widget=RecordsWidget(
            label='Immunization History',
            description=_("A list of immunizations administered to the patient."),
            visible=False,# uses view from browser/patient.py
        ),
    ),
    RecordsField('TravelHistory',
        type='travelhistory',
        subfields=('TripStartDate','TripEndDate','Country','Location','Remarks'),
        required_subfields=('Country'),
        subfield_labels={'TripStartDate':_('Trip Start Date','Start date'),
                         'TripEndDate':_('Trip End Date','End date'),
                         'Country':_('Country'),
                         'Location':_('Location'),
                         'Remarks':_('Remarks')},
        subfield_sizes={'TripStartDate':10,
                        'TripEndDate':10,
                        'Country':20,
                        'Location':20,
                        'Remarks':25},
        widget=RecordsWidget(
                label='Travel History',
                description=_("A list of places visited by the patient."),
                visible=False,
        ),
    ),

    RecordsField('ChronicConditions',
        type='chronicconditions',
        subfields=('Code','Title','Description','Onset','End','Remarks'),
        required_subfields=('title'),
        subfield_sizes={'Code':7,'Title':15,'Description':25,'Onset':7,'End':7,'Remarks':25},
        widget=RecordsWidget(
            label='Past Medical History',
            description=_("Patient's past medical history."),
            visible=False,# uses view from browser/patient.py
        ),
    ),
    StringField('BirthPlace',schemata='Personal',
        widget=StringWidget(
            label=_('Birth place'),
        ),
    ),
    StringField('Ethnicity',schemata='Personal',
        index='FieldIndex',
        vocabulary = ETHNICITIES,
        widget=ReferenceWidget(
            label=_('Ethnicity'),
            description=_("Ethnicity eg. Asian, African, etc."),
        ),
    ),
    StringField('Citizenship',schemata='Personal',
        widget=StringWidget(
            label=_('Citizenship'),
        ),
    ),
    StringField('MothersName',schemata='Personal',
        widget=StringWidget(
            label=_('Mothers name'),
        ),
    ),
    StringField('CivilStatus',schemata='Personal',
        widget=StringWidget(
            label=_('Civil status'),
        ),
    ),
    ImageField('Photo',schemata='Identification',
        widget=ImageWidget(
            label=_('Photo'),
        ),
    ),
    ImageField('Feature',schemata='Identification',
        multiValue=1,
        widget=ImageWidget(
            label=_('Feature'),
        ),
    ),
))

schema['JobTitle'].widget.visible=False
schema['Department'].widget.visible=False
schema['BusinessPhone'].widget.visible=False
schema['BusinessFax'].widget.visible=False
# Don't make title required - it will be computed from the Person's Fullname
schema['title'].required=0
schema['title'].widget.visible=False
schema['EmailAddress'].schemata='Personal'
schema['HomePhone'].schemata='Personal'
schema['MobilePhone'].schemata='Personal'
#schema.moveField('PatientID', pos='top')
schema.moveField('PrimaryReferrer',after='Surname')
schema.moveField('Gender',after='PrimaryReferrer')
schema.moveField('PatientID',before='title')

class Patient(Person):
    implements(IPatient)
    security=ClassSecurityInfo()
    displayContentsTab=False
    schema=schema

    _at_rename_after_creation=True
    def _renameAfterCreation(self,check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        """ Return the Fullname as title """
        return self.getFullname()

    security.declarePublic('getPatientID')
    def getPatientID(self):
        return self.getId()

    security.declarePublic('getSamples')
    def getSamples(self):
        """ get all samples taken from this Patient """
        bc=getToolByName(self,'bika_catalog')
        return [p.getObject() for p in bc(portal_type='Sample',getPatientUID=self.UID())]

    security.declarePublic('getARs')
    def getARs(self,analysis_state):
        bc=getToolByName(self,'bika_catalog')
        return [p.getObject() for p in bc(portal_type='AnalysisRequest',getPatientUID=self.UID())]

    def get_clients(self):
        ## Only show clients to which we have Manage AR rights.
        mtool=getToolByName(self,'portal_membership')
        clientfolder=self.clients
        clients=[]
        for client in clientfolder.objectValues("Client"):
            if not mtool.checkPermission(ManageAnalysisRequests,client):
                continue
            clients.append([client.UID(),client.Title()])
        clients.sort(lambda x,y:cmp(x[1], y[1]))
        return DisplayList(clients)

    def getPatientIdentifiersStr(self):
        ids=self.getPatientIdentifiers()
        idsstr=''
        for id in ids:
            idsstr+=idsstr=='' and id['Identifier'] or (', '+id['Identifier'])
        return idsstr
        #return self.getSendersPatientID()+" "+self.getSendersCaseID()+" "+self.getSendersSpecimenID()

    def getAgeSplitted(self):

        if (self.getBirthDate()):
            dob=DT2dt(self.getBirthDate()).replace(tzinfo=None)
            now=datetime.today()

            currentday=now.day
            currentmonth=now.month
            currentyear=now.year
            birthday=dob.day
            birthmonth=dob.month
            birthyear=dob.year
            ageday=currentday-birthday
            agemonth=0
            ageyear=0
            months31days=[1,3,5,7,8,10,12]

            if (ageday<0):
                currentmonth-=1
                if (currentmonth<1):
                    currentyear-=1
                    currentmonth=currentmonth+12;

                dayspermonth=30;
                if currentmonth in months31days:
                    dayspermonth=31;
                elif currentmonth==2:
                    dayspermonth=28
                    if(currentyear%4==0
                       and (currentyear%100>0 or currentyear%400==0)):
                        dayspermonth+=1

                ageday=ageday+dayspermonth

            agemonth=currentmonth-birthmonth
            if (agemonth<0):
                currentyear-=1
                agemonth=agemonth+12

            ageyear=currentyear-birthyear

            return {'year':ageyear,
                    'month':agemonth,
                    'day':ageday}
        else:
            return {'year':'',
                    'month':'',
                    'day':''}

    def getAge(self):
        return self.getAgeSplitted()['year']

    def getAgeSplittedStr(self):
        splitted=self.getAgeSplitted()
        arr=[]
        arr.append(splitted['year'] and str(splitted['year'])+'y' or '')
        arr.append(splitted['month'] and str(splitted['month'])+'m' or '')
        arr.append(splitted['day'] and str(splitted['day'])+'d' or '')
        return ' '.join(arr)

    def setCountryState(self, value):
        pa = self.getPhysicalAddress() and self.getPhysicalAddress() or {'country': '', 'state': ''}
        pa['country'] = self.REQUEST.form['CountryState']['country']
        pa['state'] = self.REQUEST.form['CountryState']['state']
        return self.setPhysicalAddress(pa)

    def getCountryState(self):
        return self.getPhysicalAddress()

atapi.registerType(Patient,PROJECTNAME)
