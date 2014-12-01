from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent

from uwosh.libraryguides.databases import VoyagerHandler
from uwosh.librarycache.core import CacheCore

from DateTime import DateTime

import httplib
import urlparse
import simplejson
import logging
logger = logging.getLogger("Plone")


class RefDBCache(CacheCore):
    
    VoyDAO = None
    
    def build(self):
        self.callrange = ""
        self.callrange_desc = ""
        self.VoyDAO = VoyagerHandler.VoyagerDAO()
        self.parent = aq_parent(aq_inner(self.context))
        self.departmentId = self.parent.getDepartmentId()
        
        self.determineCallRange()
        self.rebuild(self.departmentId)
        return {"departmentsRef":self.databases,
                "librarian":self.librarian,
                "voyager":self.cacheVoyagerBooks,
                "callrange":self.callrange,
                "callrange_description":self.callrange_desc,
                }

    def rebuild(self,dept_id):
        
        # Rebuild Reference Databases
        self.get_ref_dbs()
    
        # Rebuild Voyager
        if len(self.parent.getCallRange()) > 0:
            self.cacheVoyagerBooks = self._getNewPublishedBooks(callRange=self.callrange) #TODO: Change later
        else:
            self.cacheVoyagerBooks = []

    def get_ref_dbs(self):
        """ Gets Reference Data """
        try:
            url = getToolByName(self.context,'portal_properties').external_resources.getProperty('reference_dbs_ws')
            u = urlparse.urlparse(url)
            
            conn = httplib.HTTPConnection(u.hostname)
            conn.request("GET", u.path + '?id=' + str(self.departmentId))
            response = conn.getresponse()
            response_data = response.read()
            
            data = simplejson.loads(response_data)
            self.librarian = data['librarian']
            self.databases = self._transform_data(data['departmentsRef'])
        except:
            self.librarian = []
            self.databases = []
        
        
    def _transform_data(self,rows):
        """ Makes sure Reference Data is properly formatted """
        results = []
        for row in rows:
            results.append({'description' : row['dept_description'],
                            'subsection' : int(row['subsection']),
                            'index' : int(row['index']),
                            'id':int(row['id']),
                            'title': row['title'],
                            'url': row['url'],
                            'is_omit_proxy': int(row['is_omit_proxy']),
                            'is_some_full_text': int(row['is_some_full_text']),
                            'section': int(row['section']),
                            'db_description': row['description'],
                            'exclude_from_guides': int(row['exclude_from_guides']),
                            'trial_message': row['trial_message'],
                            'warning_message': row['warning_message'],
                            'tutorial_url': row['tutorial_url'],
                            'gots_url': row['gots_url'],
                           })
        return results
    
    
    def determineCallRange(self):
        # DAY MOD CALLPOS
        crl = self.parent.getCallRange()
        i = len(crl)
        if i > 0:
            cr = crl[(DateTime().dayOfYear() % i)]
            self.callrange = cr['callnumber']
            self.callrange_desc = cr['classification']


    def _getNewPublishedBooks(self,callRange=None,xml=False):
        if xml:
            self.VoyDAO.voyagerSearchService(searchCode="CALL+",searchArg=callRange,searchArgType="AND",displayRelevanceFlag="N",maxResultsPerPage="3")
            return self.VoyDAO.voyagerSearchResultsService(searchType="FIND",resultPointer="0",maxResultsPerPage="25",sortBy="PUB_DATE_DESC")
        else:
            self.VoyDAO.voyagerSearchService(searchCode="CALL+",searchArg=callRange,searchArgType="AND",displayRelevanceFlag="N",maxResultsPerPage="3")
            xml = self.VoyDAO.voyagerSearchResultsService(searchType="FIND",resultPointer="0",maxResultsPerPage="25",sortBy="PUB_DATE_DESC")
            return self.ebooks(self.weeder(self.VoyDAO.xmlToList(xml),3))
        
        
    def ebooks(self,listing):
        """ length > 4 for Leisure  |  find('/') for gov """
        results = []
        for l in listing:
            l['ebook'] = False
            if '[electronic resource]' in l['title'] or '[computer file]' in l['title']:
                l['ebook'] = True
            l['title_clean'] = l['title_clean'].replace('[electronic resource]','').replace('[computer file]','')
            l['title'] = l['title'].replace('[electronic resource]','').replace('[computer file]','')
            results.append(l)
        return results
        
    def weeder(self,listing,limit):
        """ length > 4 for Leisure  |  find('/') for gov """
        results = []
        i = 0
        for l in listing:
            if i == limit:
                break
            if len(l['callnumber']) > 4 and l['callnumber'].find('/') == -1 and not self._isDuplicate(results,l['bibId']):
                results.append(l)
                i += 1
        return results
        
        
    def _isDuplicate(self,listing,item):
        for l in listing:
            if l['bibId'] == item:
                return True
        return False
        
        