from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements, Interface
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.memoize import ram

from uwosh.libraryguides.browser import util

from DateTime import DateTime
from time import time
from operator import itemgetter


class SubjectFactory(object):

    @classmethod
    def parse_cache(cls, section, cache, limit=1000):
        """ parses all databases based off of categories. """
        data = cache['departmentsRef']
        results = sorted(data,key=itemgetter('subsection','index'))
        return filter(lambda x:  x['section'] == section, results)[0:limit]

    @classmethod
    def _safe_pop(self,lists,start,end):
        """ Safely pop lists, even if empty """
        try:
            if len(lists) >= end:
                return lists[start:end]
            else:
                return lists[start:len(lists)]
        except:
            return []


class GuideTemplateTools(BrowserView):
    
    def EzProxy(self,omit_proxy,url):
        proxy_url = getToolByName(self.context, 'portal_properties').get('external_resources',None).getProperty('proxy_server_url','')
        if not bool(omit_proxy):
            return proxy_url + url
        else:
            return url
    
    def shorten_text(self,text,limit):
        return text[:limit] + '...' if len(text) > limit else text
    
    def image_type(self,number):
        """ Hate this function, assigns a image and type to a resource """
        if number == 1:
            return {"image":"++resource++uwosh.librarytheme.images/background_info.png","title":"Reference and Background Resources"}
        elif number == 2:
            return {"image":"++resource++uwosh.librarytheme.images/books.png","title":"Book Resources"}
        elif number == 3:
            return {"image":"++resource++uwosh.librarytheme.images/journals.png","title":"Journal, Magazine and Newspaper Resources"}
        elif number == 4:
            return {"image":"++resource++uwosh.librarytheme.images/primary_source.png","title":"Primary Source Resources"}
        else:
            return {"image":"","title":"Resource"}


class SubjectBaseView(GuideTemplateTools):
    """
    This is the base controller class for all subject guides views.
       
    @author: David Hietpas
    @version: 0.0.2
    """
    
    cache = {}
    books = []
    research_databases = []
    references = []
    primary_sources = []
    campus_resources = []
    voyager_books = []
    voyager_books_ranges = ""
    voyager_books_range_title = ""
    
    def __init__(self,context,request):
        super(SubjectBaseView, self).__init__(context,request)
        self.cache = self._get_cache()
        if self.cache != {}:
            self.references = SubjectFactory.parse_cache(1, self.cache)
            self.books = SubjectFactory.parse_cache(2, self.cache)
            self.research_databases = SubjectFactory.parse_cache(3, self.cache)
            self.primary_sources = SubjectFactory.parse_cache(4, self.cache)
            self.campus_resources = SubjectFactory.parse_cache(5, self.cache)
            self.voyager_books = self.cache['voyager']
            self.voyager_books_ranges = self.cache['callrange']
            self.voyager_books_range_title = self.cache['callrange_description']
        
    def _get_cache(self):
        """ Get cache object, wakes object, try to call this once. """ 
        query = util.getGuidesPath(self) + "/" + self.context.id
        brains = getToolByName(self.context, 'portal_catalog').searchResults(portal_type=('LibraryCache'), path={'query':query},
                                                                             sort_on="modified", sort_order='descending', limit=1)
        if len(brains) > 0:
            return brains[0].getObject().getCache()
        return {}

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


class SubjectGuideView(SubjectBaseView):
    """
    This controller class extends and adds functionality for the main subject guide view.  
    @author: David Hietpas
    @version: 1.1
    """
    featured_database = {}
    
    def __init__(self,context,request):
        super(SubjectGuideView, self).__init__(context,request)
        
        self.databases = SubjectFactory._safe_pop(self.research_databases,0,3) + SubjectFactory._safe_pop(self.books,0,1) + \
                         SubjectFactory._safe_pop(self.primary_sources,0,1)
                         
        remaining_databases = SubjectFactory._safe_pop(self.research_databases,3,999) + SubjectFactory._safe_pop(self.books,1,999) + \
                                  SubjectFactory._safe_pop(self.primary_sources,1,999)
        if remaining_databases:
            self.featured_database = remaining_databases[(DateTime().dayOfYear() % len(remaining_databases))]
    
    
    def getNewNewsItems(self):
        """ Retrieves news items with site set criteria """
        timespan = getToolByName(self.context, 'portal_properties').get('site_properties').getProperty('news_limit_days',90)
        from_start = DateTime() - timespan
        brains = getToolByName(self.context, 'portal_catalog').searchResults(portal_type='WeblogEntry',
                                                                             Subject=self.context.getNewsTopic(),
                                                                             sort_on='created',
                                                                             sort_order='descending',
                                                                             review_state='published',
                                                                             created={'query':(from_start,DateTime('2045-11-19 11:59:00')),
                                                                                               'range': 'min:max'}
                                                                             )
        return brains[:3]
        

    def isOnCampus(self):
        """ Determines if someone is on campus via IP, this function might be moved later. """
        
        ip_range = getToolByName(self.context, 'portal_properties').get('library_ip_ranges').getProperty('campus_ip_range', '0.0.0.0')

        if 'HTTP_X_FORWARDED_FOR' in self.request.environ:
            ip = self.request.environ['HTTP_X_FORWARDED_FOR'] # Virtual host
        elif 'HTTP_HOST' in self.request.environ:
            ip = self.request.environ['REMOTE_ADDR'] # Non-virtualhost
        else:
            ip = "0.0.0.0"
        
        ip = ip.split(',')[0].strip()
        
        return ip.startswith(ip_range)
  
  
class ResearchDatabasesView(SubjectBaseView):
    """
    This controller class extends and adds functionality for the research databases view.  
    @author: David Hietpas
    @version: 0.0.2
    """
    
    def get_databases(self):
        """ Combines all databases in different categories and sorts them """
        databases = self.books + self.primary_sources + self.research_databases
        return sorted(databases,key=itemgetter('subsection','index'))
    
    def get_highly_recommended(self):
        """ Re-groups all databases """
        return filter(lambda x: x['subsection'] == 1, self.get_databases())
    
    def get_also_useful(self):
        """ Re-groups all databases """
        return filter(lambda x: x['subsection'] == 2, self.get_databases())


class SubViewHook(BrowserView):
    """ This hook class allows hand off of data through subviews. """
    def __call__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        return super(SubViewHook, self).__call__()


