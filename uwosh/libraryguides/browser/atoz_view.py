from zope.interface import implements, Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize import ram
from uwosh.libraryguides.browser.subject_view import GuideTemplateTools
from time import time
import logging
logger = logging.getLogger("Plone")

class IATOZView(Interface):
    """ Interface Marker """

class ATOZView(GuideTemplateTools):
    """ View for A-to-Z Database listing.  Context is a LibraryCache Object """
    
    def __call__(self):
        """ Get criteria for viewing content """
        self._crit_start = self.request.form.get('display','a').lower()
        self._crit_end = self.request.form.get('through',self._crit_start).lower()
        self.getABCHeaderList()
        return super(ATOZView,self).__call__()

    @ram.cache(lambda *args: time() // (60 * 60 * 24))
    def getABCHeaderList(self):
        """ Creates ABCDEF..XYZ listing based on content """
        items = set(self.get(filter=False,char=True))
        return sorted(items)

    def get(self,filter=True,char=False):
        """ Get criteria for viewing content """
        filtered = []
        for item in self.context.getCache():
            if filter and self.filter(item):
                filtered.append(item)
                filtered = sorted(filtered, key=lambda x: x['title'].lower())
            elif char:
                filtered.append(item['title'][0].lower())
        return filtered
    
    def filter(self,item=None,char=None):
        c = '!'
        if item != None:
            c = item['title'][0].lower()
        if char != None:
            c = char
        if ord(c) >= ord(self._crit_start) and ord(c) <= ord(self._crit_end):
            return True
        return False
        
    def title_to_id(self,title):
        title = filter(lambda x: x.isdigit() or x.isalpha() or x.isspace(), title)
        return title.replace(" ", "-")
        
    @property
    def portal(self):
        return getToolByName(self.context,'portal_url').getPortalObject()
