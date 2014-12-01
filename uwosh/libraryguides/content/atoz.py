from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent

from uwosh.librarycache.core import CacheCore

from DateTime import DateTime
from operator import itemgetter

import httplib
import urlparse
import simplejson

class ATOZ(CacheCore):

    def build(self):
        self._doATOZQuery()
        return sorted(self.atoz_list,key=itemgetter('title'))

    def _doATOZQuery(self):
        """ Calls the db for the result set.  It is then filtered down to almost half the size by for loop. """
        try:
            url = getToolByName(self.context,'portal_properties').external_resources.getProperty('atoz_ws')
            u = urlparse.urlparse(url)
            
            conn = httplib.HTTPConnection(u.hostname)
            conn.request("GET", u.path)
            response = conn.getresponse()
            response_data = response.read()
            
            data = simplejson.loads(response_data)
            self.atoz_list = self._transform_data(data['atoz_list'])
        except:
            self.atoz_list = []

    def _transform_data(self,rows):
        results = []
        s = set() # ensures one of a kind.
        for row in rows:
            if str(row['url']).strip() not in s:
                s.add(str(row['url']).strip())
                results.append({'section':int(row['section']),
                                'id':row['id'],
                                'title':row['title'],
                                'url':row['url'],
                                'is_omit_proxy':int(row['is_omit_proxy']),
                                'is_some_full_text':int(row['is_some_full_text']),
                                'db_description':row['description'],
                                'trial_message':row['trial_message'],
                                'warning_message':row['warning_message'],
                                'tutorial_url': row['tutorial_url'],
                                'gots_url': row['gots_url'],
                                'coverage':row['coverage'],
                                'vendor':row['vendor'],
                                })
        return results


