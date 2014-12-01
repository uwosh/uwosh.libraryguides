from zope import schema
from zope.interface import Interface,implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base, folder, schemata
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from Products.validation.validators.ExpressionValidator import ExpressionValidator

from Products.Archetypes.atapi import StringField,StringWidget,IntegerField,IntegerWidget,LinesField,InAndOutWidget,PicklistWidget,LinesField,LinesWidget,SelectionWidget
from uwosh.libraryguides import libraryguidesMessageFactory as _
from uwosh.libraryguides.config import PROJECTNAME
from uwosh.libraryguides.browser import util

from datetime import datetime

import logging
logger = logging.getLogger("Plone")

class ILibrarySubjectGuide(Interface):
    """a form to request a query"""

"""
This is a standard extension of a Plone Schema, see books or tutorials.
Note: Schema does not extend the ATCTBTreeFolder but the one below does
"""
LibrarySubjectGuideSchema = folder.ATBTreeFolderSchema.copy() + atapi.Schema(( 
                         
        IntegerField('departmentId',
            required=True,
            searchable=False,
            default = "",
            validators = ('isInt'),
            widget = IntegerWidget(
                description = "Department ID is the primary_key for Departments in the CoursePages Database.  Please match this to the correct field.",
                label = _(u'Department ID', default=u'Department ID'),
            )),
        
        atapi.TextField('searchBox',
            required=False,
            searchable=False,
            default = "",
            widget = atapi.TextAreaWidget(
                description = "Required Format is 'URL|QueryParameter|Method'. Example: 'http://url.com?extra=params|query_parameter_name|POST'",
                label = _(u'Search Box Setup', default=u'Search Box Setup'),
            )),
            
        LinesField('callRange',
            required=False,
            searchable=False,
            default = "",
            validators = (),
            widget = LinesWidget(
                description = "LC Classification for this subject. Please use the format 'SubClass|Classification Description' without the single quotes. Example: 'QE|Geology'",
                label = _(u'Department Call Range', default=u'Department Call Range'),
            )),
            
        LinesField('journalListListing',
            required=False,
            searchable=False,
            default = "",
            validators = (),
            widget = LinesWidget(
                description = "Journal Listings for this subject.  Please use the format 'JournalName|JournalLink' without the single quotes.  Example: 'Journals in Biology|http://www.example.com'",
                label = _(u'Journal Listings', default=u'Journal Listings'),
            )),
            
            
        StringField('newsFeed',
            required=True,
            searchable=False,
            default = "",
            validators = (),
            vocabulary="getKeywords",
            widget = SelectionWidget(
                description = "The news section will pull any News related to this tag name.  Uses tag names. ",
                label = _(u'Primary News Topic', default=u'Primary News Topic'),
            )),
            
            
        StringField('governmentMoreLink',
            required=False,
            searchable=False,
            default = "",
            validators = (),
            widget = StringWidget(
                description = "This is More Link for the Government Section.",
                label = _(u'Government More Link', default=u'Government More Link'),
            )),
            
        LinesField('governmentLinkList',
            required=False,
            searchable=False,
            multiValued=True,
            vocabulary="getGovernmentListVocab",
            enforceVocabulary=True,
            widget = PicklistWidget(
                description = "Select Links to be displayed in the Government Section.",
                label = _(u'Government Section Links', default=u'Government Section Links'),
            )),  
            
            
        StringField('emcMoreLink',
            required=False,
            searchable=False,
            default = "",
            validators = (),
            widget = StringWidget(
                description = "This is More Link in the EMC Section.",
                label = _(u'EMC More Link', default=u'EMC More Link'),
            )),
            
        LinesField('emcLinkList',
            required=False,
            searchable=False,
            multiValued=True,
            vocabulary="getEMCListVocab",
            enforceVocabulary=True,
            widget = PicklistWidget(
                description = "Select Links to be displayed in the EMC Section.",
                label = _(u'EMC Section Links', default=u'EMC Section Links'),
            )),  
            
        StringField('archivesMoreLink',
            required=False,
            searchable=False,
            default = "",
            validators = (),
            widget = StringWidget(
                description = "This is More Link in the Archives Section.",
                label = _(u'Archives More Link', default=u'Archives More Link'),
            )),
            
        LinesField('archivesLinkList',
            required=False,
            searchable=False,
            multiValued=True,
            vocabulary="getArchivesListVocab",
            enforceVocabulary=True,
            widget = PicklistWidget(
                description = "Select Links to be displayed in the Archives Section.",
                label = _(u'Archives Section Links', default=u'Archives Section Links'),
            )),  
                                                                              
                                                                              
        StringField('filmsOnDemandMoreLink',
            required=False,
            searchable=False,
            default = "",
            validators = (),
            widget = StringWidget(
                description = "This is the more link for Films on Demand.  IT IS PROXIED AUTOMATICALLY",
                label = _(u'Films on Demand More Link', default=u'Films on Demand More Link'),
            )),
            
        LinesField('filmsOnDemandList',
            required=False,
            searchable=False,
            default = "",
            validators = (),
            widget = LinesWidget(
                description = "Put one id number per line.",
                label = _(u"List of Films on Demand ID's", default=u"List of Films on Demand ID's"),
            )),
                                                                                       
                                                                              
))

LibrarySubjectGuideSchema['title'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['description'].storage = atapi.AnnotationStorage()

LibrarySubjectGuideSchema['title'].widget.label = 'Library Subject Guide'
LibrarySubjectGuideSchema['description'].widget.description = 'Not used.'
LibrarySubjectGuideSchema['description'].required = False

LibrarySubjectGuideSchema['departmentId'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['callRange'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['journalListListing'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['newsFeed'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['governmentMoreLink'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['governmentLinkList'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['emcMoreLink'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['emcLinkList'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['archivesMoreLink'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['archivesLinkList'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['filmsOnDemandMoreLink'].storage = atapi.AnnotationStorage()
LibrarySubjectGuideSchema['filmsOnDemandList'].storage = atapi.AnnotationStorage()


# Hide Sections.
LibrarySubjectGuideSchema['description'].widget.visible={'view':'invisible', 'edit':'invisible'}
LibrarySubjectGuideSchema['subject'].mutator="setNewsCriteria"
LibrarySubjectGuideSchema['location'].widget.visible={'view':'invisible', 'edit':'invisible'}
LibrarySubjectGuideSchema['language'].widget.visible={'view':'invisible', 'edit':'invisible'}


schemata.finalizeATCTSchema(LibrarySubjectGuideSchema, moveDiscussion=False)
LibrarySubjectGuideSchema.changeSchemataForField('relatedItems', 'default')




class LibrarySubjectGuide(base.ATCTBTreeFolder):
    """
    Library Guide Folder ContentType.  Customized to allow for Guide Setup and Caching.
    @author: David Hietpas
    @version: 1.0
    """
    implements(ILibrarySubjectGuide)

    meta_type = "LibraryGuideFolder"
    schema = LibrarySubjectGuideSchema
    
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
  

    def getDepartmentID(self):
        """
        Gets Department Number from Object.
        @return: string, Department Number
        """
        return self.getField('departmentId').get(self)
    
    def getCallRange(self):
        """
        Gets CallRange from Object to match against Voyager Catalog
        @return: string or tuple, callrange identifications
        """
        crl = self.getField('callRange').get(self)
        results = []
        try:
            for cr in crl:
                results.append(util.formatDelimited(cr, ['callnumber','classification']))
        except Exception as e:
            logger.error(e)
        return results
    

    def getTitle(self):
        """
        Gets Department Title, such as Physics or Chemistry
        @return: string, Department Title
        """
        return self.getField('title').get(self)

    def getNewsTopic(self):
        return self.getField('newsFeed').get(self)


    def getJournalListings(self):
        """
        Gets Journal Listing Name from object, goes with getJournalListingURL()
        @return: string, is name of Journal Listing URL
        """
        jln = self.getField('journalListListing').get(self)
        results = []
        try:
            for jl in jln:
                results.append(util.formatDelimited(jl, ['Title','getURL']))
        except Exception as e:
            logger.error(e)
        return results
    
    def setNewsCriteria(self,value):
        self.getField('subject').set(self,tuple(value))

    def getGovernmentMoreContent(self):
        """
        Gets the Governments (more) URL on the guide page.
        @return: string, is a URL for the (more) link
        """            
        return self.getField('governmentMoreLink').get(self)
    

    def getGovernmentListContent(self):
        """
        Gets the Governments Query criteria for the Listing of Links under
        government section.
        @return: list of string, is list of strings which are portal_catalog 
        path (example: /library/example/item/)
        """
        links = self.getField('governmentLinkList').get(self)
        return self.queryLinkObjects(links)

    def getGovernmentListVocab(self): 
        """
        Creates the Vocabulary needed for the Government PickList.  Used above in 
        schema governmentLinkList.
        @return: list of tuples, is a list of tuples of [(value,content),] for 
                multi-optional widgets  which use the <option/> tags
        """    
        results = []
        try:
            catalog = getToolByName(self, "portal_catalog")
            brains = catalog.searchResults(path=util.getGovernmentPath(self),
                                           sort_on="sortable_title",
                                           )
            brains = self._filter(brains)
            for brain in brains:
                tup = brain.getPath(),unicode(brain.Title,errors="replace") + " ("+brain.Type+")"
                results.append(tup)
        except Exception as e:
            pass
        return results

    def getEMCMoreContent(self):
        """
        Gets the EMC (more) URL on the guide page.
        @return: string, is a URL for the (more) link
        """
        return self.getField('emcMoreLink').get(self)
    
    def getEMCListContent(self):
        links = self.getField('emcLinkList').get(self)
        return self.queryLinkObjects(links)
    
    def getEMCListVocab(self):
        """
        Creates the Vocabulary needed for the EMC PickList.  Used above in 
        schema emcLinkList.
        @return: list of tuples, is a list of tuples of [(value,content),] for 
                multi-optional widgets  which use the <option/> tags
        """
        results = []
        try:
            catalog = getToolByName(self, "portal_catalog")
            brains = catalog.searchResults(path=util.getEMCPath(self),
                                           sort_on="sortable_title",
                                           )
            brains = self._filter(brains)
            for brain in brains:
                tup = brain.getPath(),unicode(brain.Title,errors="replace") + " ("+brain.Type+")"
                results.append(tup)
        except Exception as e:
            pass
        return results

    def getArchivesMoreContent(self):
        """
        Gets the Archives (more) URL on the guide page.
        @return: string, is a URL for the (more) link
        """
        return self.getField('archivesMoreLink').get(self)
    
    def getArchivesListVocab(self):
        """
        Creates the Vocabulary needed for the EMC PickList.  Used above in 
        schema emcLinkList.
        @return: list of tuples, is a list of tuples of [(value,content),] for 
                multi-optional widgets  which use the <option/> tags
        """
        results = []
        try:
            catalog = getToolByName(self, "portal_catalog")
            brains = catalog.searchResults(path=util.getArchivesPath(self),
                                           sort_on="sortable_title",
                                           )
            brains = self._filter(brains)
            for brain in brains:
                tup = brain.getPath(),unicode(brain.Title,errors="replace") + " ("+brain.Type+")"
                results.append(tup)
        except Exception as e:
            pass
        return results
    
    def getArchivesListContent(self):
        """
        Gets the Archives Query criteria for the Listing of Links under
        Archives section.
        @return: list of string, is list of strings which are portal_catalog 
        path (example: /library/example/item/)
        """
        links = self.getField('archivesLinkList').get(self)
        return self.queryLinkObjects(links)


    def getKeywords(self):
        index = getToolByName(self, "portal_catalog")._catalog.getIndex('Subject')
        results = []
        for i in index._index:
            tup = str(i),str(i) # Setup Tuple.
            results.append(tup)
        return results

    def getAllLinks(self,results=None):  
        """
        Extends the List of Tuples from the Vocabularies EMC and Government.  It adds
        all site Links to those Vocabularies.  This is used only for Vocabularies.
        @param results: is a list of tuples, that will be extended by this function
        @return: list of tuples, is a list of tuples of [(value,content),] for 
                multi-optional widgets  which use the <option/> tags
        """
        if results == None:
            results = []
        else:
            tup = "None","------------------------------"
            results.append(tup)
            
        try:
            catalog = getToolByName(self, "portal_catalog")
            brains = catalog.searchResults(portal_type='LibraryLinks',
                                           sort_on="sortable_title",
                                           )
            brains = self._filter(brains)
            for brain in brains:
                tup = brain.getPath(),unicode(brain.Title,errors="replace") + " ("+brain.Type+")"
                results.append(tup)
        except Exception as e:
            pass
        return results
    
    def _filter(self,items):
        seen = set()
        filtered = list()
        for item in items:
            if item['portal_type'] == "LibraryLinks":
                key = item['getRemoteUrl']
                if key not in seen:
                     seen.add(key)
                     filtered.append(item)
            else:
                filtered.append(item)
        return filtered
    
    def getSearchBoxData(self):
        try:
            val = self.getField('searchBox').get(self)
            return util.formatDelimited(val, ['action','query','method'])
        except Exception as e:
            print "Error " + str(e)
            return None
        
    def queryLinkObjects(self, queries):
        results = []
        for query in queries:
            if query != "None":
                brains = getToolByName(self, 'portal_catalog').searchResults(path={'query':query, 'depth':0})
                if len(brains) > 0:
                    results.append({"name":brains[0].Title, "url":brains[0].getURL(), "Description":brains[0].Description})
        return results
        
    def fetch(self):
        val = self.getField('searchBox').get(self)
        return tuple(val.split('|'))
    
    def getNextFilm(self):
        try:
            films = self.getField('filmsOnDemandList').get(self)
            day_of_year = datetime.now().timetuple().tm_yday
            index = day_of_year % len(films)
            parts = films[index].split('|')
            return {'id':parts[0].strip(),'Title':parts[1].strip()}
        except Exception as e:
            return None
    
    def getProxiedFilmsOnDemandMoreLink(self):
        proxy = getToolByName(self, "portal_properties").get('external_resources').getProperty('proxy_server_url')
        return proxy + str(self.getField('filmsOnDemandMoreLink').get(self)).strip()
        
    def showFilmsOnDemand(self):
        return (self.getFilmsOnDemandMoreLink().strip() != "") and (len(self.getField('filmsOnDemandList').get(self)) > 0)
    
    
    
atapi.registerType(LibrarySubjectGuide, PROJECTNAME)