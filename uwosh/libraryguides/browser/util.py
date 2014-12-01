from zope.interface import implements, Interface, Attribute
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime



def formatDelimited(content,keys,delimiter="|"):
    parts = content.split(delimiter)
    data = {}
    for k in range(len(keys)):
        try:
            data[keys[k]] = parts[k].strip()
        except:
            data[keys[k]] = ''
    return data
    
    
def EzProxy(context,omit_proxy=False):
    """
    Plugin Function Example:
    class Foo:
        global_var = checkAndGetProxy #calling global_var will now call checkAndGetProxy
        
    This will make context as self.
    """
    props = getToolByName(context, 'portal_properties').get('external_resources',None)
    if props != None:
        proxy_url = props.getProperty('proxy_server_url','')
        if not bool(omit_proxy):
            return proxy_url
        else:
            return ""
    
    
def getGuidesPath(context):
    """
    Calls portal_properties and gets the base path of the guides folder.
    @return: string, the relative location of the guides.
    """
    props = getToolByName(context, 'portal_properties')
    return props.base_paths.getProperty('base_guide_path')

def getEMCPath(self):
    """
    Calls portal_properties and gets the base path of the emc folder.
    @return: string, the relative location of the emc.
    """
    props = getToolByName(self, 'portal_properties')
    return props.base_paths.getProperty('base_emc_path')

def getGovernmentPath(self):
    """
    Calls portal_properties and gets the base path of the government folder.
    @return: string, the relative location of the government.
    """
    props = getToolByName(self, 'portal_properties')
    return props.base_paths.getProperty('base_government_path')

def getArchivesPath(self):
    """
    Calls portal_properties and gets the base path of the government folder.
    @return: string, the relative location of the government.
    """
    props = getToolByName(self, 'portal_properties')
    return props.base_paths.getProperty('base_archives_path')


def getAtoZPath(self):
    """
    Calls portal_properties and gets the base path of the government folder.
    @return: string, the relative location of the government.
    """
    props = getToolByName(self, 'portal_properties')
    return props.base_paths.getProperty('base_atoz_path')



def securityIsModifier(context,request,redirect=False):  
    """
    Determines if the user has management rights.  If does returns True, if not False.
    If specified "redirect=True" the function will redirect if user does not have
    management rights.
    @param context: Current context the user is in.
    @param request: Current page request.
    @param redirect: Redirects to homepage if True and user has no management rights.
    @return: True if User has management rights, False if user has no management rights.
    """
    isMod = False
    if context.portal_membership.checkPermission('Modify portal content', context):
        isMod = True
    if not isMod and redirect: 
        request.response.redirect(getToolByName(context, 'portal_url').getPortalObject().absolute_url())
    return isMod


def getGuidesListing(context):
    """
    Gets the Listing of Guides.
    @param context: callers current context. 
    @return: list
    """
    brains = getToolByName(context, 'portal_catalog').searchResults(portal_type='LibrarySubjectGuide',sort_on='sortable_title')
    results = []
    for brain in brains:
        parts = list(brain.fetch)
        if len(parts) != 3:
            parts = ['','','']
        searchBox = {'searchURL':parts[0],'queryParam':parts[1],'methodAction':parts[2]}
        results.append({"url": brain.getURL(),"title": brain.Title,"id": brain.id,'searchBox':searchBox})
    return results

def getGuidesListingByTags(context):
    """ Gets all subject guides Tagged with SubjectGuide Tag """
    path = getGuidesPath(context)
    guides = getToolByName(context, 'portal_catalog').searchResults(portal_type=['LibrarySubjectGuide','Document'],
                                                                         path={'query':path,'depth':10},
                                                                         Subject=('Subject Guide','Subject Guides'),
                                                                         sort_on='sortable_title')
    return guides


""" DAO's BELOW ------------------------------------------------ """

class ILibraryDAO(Interface):
    context = Attribute("""Object Context""")
    def get(self,**kwargs):
        """ Depending on the DAO, this will return the results """
