
# Load fixture
from Testing import ZopeTestCase

import unittest
from uwosh.libraryguides.tests.base import TestCase
from Products.CMFCore.utils import getToolByName

class ViewsTest(TestCase):

    def afterSetUp(self):
        
        self.folder.invokeFactory('LibrarySubjectGuide', id='geo',title='geo title')
        self.folder.geo.setOneSearchId(12345)
        self.folder.geo.setEmcMoreLink("http://www.example1.com")
        self.folder.geo.setArchivesMoreLink("http://www.example2.com")
        self.folder.geo.setGovernmentMoreLink("http://www.example3.com")

        self.folder.geo.invokeFactory('LibraryCache', id='cache',title='Cache')
        self.folder.geo.cache.masterCache = {'voyager':['1','2'],
                                             'callrange':'Q|NamedSubject',
                                             'callrange_description':'test',
                                             'departments':[],
                                             'departmentsRef':[]
                                             }
        self.guide_view = self.folder.geo.unrestrictedTraverse('guide_view')
        self.guide_view.context = self.folder.geo
        self.guide_view.cache = self.folder.geo.cache
        
        
    def test_creation(self):
        self.assertEquals(self.folder.geo.title,'geo title')
        
    def test_creation_false(self):
        self.assertNotEqual(self.folder.geo.title,'geo false')

    def test_onesearch(self):
        self.assertEquals(self.folder.geo.getOneSearchId(),12345)

    def test_morelink1(self):
        self.assertEquals(self.folder.geo.getEmcMoreLink(),"http://www.example1.com")

    def test_morelink2(self):
        self.assertEquals(self.folder.geo.getArchivesMoreLink(),"http://www.example2.com")

    def test_morelink3(self):
        self.assertEquals(self.folder.geo.getGovernmentMoreLink(),"http://www.example3.com")
        
        
        
    def test_registered_view(self):
        view = self.folder.geo.unrestrictedTraverse('guide_view')
        self.assertEquals(view.isNewsVisible,False)
        
    def test_cached_books(self):
        self.guide_view.handleBooksContent()
        self.assertEquals(self.guide_view.isBooksVisible,True)
        
    def test_cached_books_callrange(self):
        self.guide_view.handleBooksContent()
        self.assertEquals(self.guide_view.books_section_callrange,"Q|NamedSubject")
        
        
        

#    def test_views(self):
#        view = self.it.unrestrictedTraverse('@@skin_layer')
#        skins = dict([(s.name, s.layers) for s in view.getSkins(False)])
#        self.failUnless('skinA' in skins, skins)
#        self.failUnless('skinB' in skins, skins)
#        self.failUnless('skinC' in skins, skins)
#        # Sort
#        [v.sort() for k, v in skins.items()]
#        layers = lambda s: [l.name for l in s]
#        self.assertEquals(layers(skins['skinA']), ['default'])
#        self.assertEquals(layers(skins['skinB']), ['layer5', 'layer4', 'default'])
#        self.assertEquals(layers(skins['skinC']), ['layer4', 'layer2',
#                                                   'layer1', 'default'])
#        # Test view details
#        request = self.it.REQUEST
#        request['iface'] = 'IFoo'
#        request['type'] = 'IBrowserRequest'
#        view = self.it.unrestrictedTraverse('@@view_details')
#        layer = view.getViewsByLayers()[0]
#        self.assertEquals(layer['name'], 'default')
#        view = layer['views'][0]
#        info = dict(view)
#        self.assertEquals(info['name'], 'index.html')
#        finfo = dict(info['factory'])
#        self.assertEquals(finfo['path'], 'test_views.FooView')
#        self.assertEquals(finfo['template'], None)
        
        
        
#
#class TestDefaultView(TestDefaultPage):
#
#    def afterSetUp(self):
#        TestDefaultPage.afterSetUp(self)
#        self.ob = self.ob.__of__(self.portal)
#
#    def getDefault(self, request=None):
#        from Products.Flon.browser import BrowserDefault
#        if request is None:
#            request = self.portal.REQUEST
#        return BrowserDefault(self.ob).defaultView(request)
#
#    def testdefaultViewPrecedence(self):
#        pres = zapi.getGlobalService('Presentation')
#        type = IBrowserRequest
#        ztapi.browserView(IFoo, 'foo.html', FooView, layer='default')
#        ztapi.browserView(IFoo, 'bar.html', FooView, layer='default')
#
#        directlyProvides(self.ob, IFoo)
#        pres.setDefaultViewName(IFoo, type, 'foo.html')
#
#        self.ob.set_default(['baz'], 0)
#
#        # baz doesn't exist, should get foo.html which exists
#        self.ob.keys = []
#        self.assertEquals(self.getDefault(), (self.ob, ['foo.html']))
#
#        # And if changed to bar, then we get bar
#        pres.setDefaultViewName(IFoo, type, 'bar.html')
#        self.assertEquals(self.getDefault(), (self.ob, ['bar.html']))
#
#        # But if baz exists, we should get baz
#        self.ob.keys = ['baz']
#        self.assertEquals(self.getDefault(), (self.ob, ['baz']))
#
#        # Now, if index_html exists, it should have precedence
#        self.ob.keys = ['index_html']
#        self.assertEquals(self.getDefault(), (self.ob, ['index_html']))
#
#        # The same for index.html
#        self.ob.keys = ['index.html']
#        self.assertEquals(self.getDefault(), (self.ob, ['index.html']))
#
#        # And for Frontpage
#        self.ob.keys = ['FrontPage']
#        self.assertEquals(self.getDefault(), (self.ob, ['FrontPage']))
#
#        # And then, if we don't implement IFoo anymore, and there's
#        # no content, we should get None, which will trigger the fallback
#        # browserDefault method.
#        directlyProvides(self.ob, IBar)
#        self.ob.keys = []
#        self.assertEquals(self.getDefault(), (self.ob, None))
#
#def get_default(ob, request=None):
#    from Products.Flon.browser import BrowserDefault
#    if request is None:
#        request = ob.REQUEST
#    return BrowserDefault(ob).defaultView(request)
#
#class TestContentDefaultView(PloneTestCase.PloneTestCase):
#
#    def test_document_default(self):
#        self.loginPortalOwner()
#        p = self.portal
#        if not 'index_html' in p.objectIds():
#            p.invokeFactory('Document', 'index_html')
#        ob = self.portal.index_html
#        self.assertEquals(ob.getPortalTypeName(), 'Document')
#        default = get_default(ob)
#        self.assertEquals(default, (ob, ['document_view']))
#
#    def test_news_default(self):
#        self.loginPortalOwner()
#        p = self.portal
#        p.invokeFactory('News Item', 'news')
#        ob = self.portal.news
#        self.assertEquals(ob.getPortalTypeName(), 'News Item')
#        default = get_default(ob)
#        self.assertEquals(default, (ob, ['newsitem_view']))
#
#    def test_folder_default(self):
#        self.loginPortalOwner()
#        p = self.portal
#        p.invokeFactory('Folder', 'test')
#        ob = self.portal.test
#        self.assertEquals(ob.getPortalTypeName(), 'Folder')
#        default = get_default(ob)
#        self.assertEquals(default, (ob, None))


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ViewsTest))
    return suite
