from DateTime import DateTime
from operator import itemgetter
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary


from uwosh.libraryguides import libraryguidesMessageFactory as _
from uwosh.libraryguides.browser import util
from uwosh.libraryguides.browser.subject_view import SubjectFactory

import htmlentitydefs
import datetime
import logging
logger = logging.getLogger("Plone")


limit_vocabulary = SimpleVocabulary([
    SimpleVocabulary.createTerm(-1, '-1', u'Show - Heading Only'),
    SimpleVocabulary.createTerm(0, '0', u'Hide - Everything'),
    SimpleVocabulary.createTerm(1, '1', u'Show - 1 item'),
    SimpleVocabulary.createTerm(2, '2', u'Show - 2 items'),
    SimpleVocabulary.createTerm(3, '3', u'Show - 3 items'),
    SimpleVocabulary.createTerm(4, '4', u'Show - 4 items'),
    SimpleVocabulary.createTerm(5, '5', u'Show - 5 items'),
    SimpleVocabulary.createTerm(1000, '1000', u'Show - Everything'),
])

limit_no_heading_vocabulary = SimpleVocabulary([
    SimpleVocabulary.createTerm(0, '0', u'Show - Nothing'),
    SimpleVocabulary.createTerm(1, '1', u'Show - 1 item'),
    SimpleVocabulary.createTerm(2, '2', u'Show - 2 items'),
    SimpleVocabulary.createTerm(3, '3', u'Show - 3 items'),
    SimpleVocabulary.createTerm(4, '4', u'Show - 4 items'),
    SimpleVocabulary.createTerm(5, '5', u'Show - 5 items'),
    SimpleVocabulary.createTerm(1000, '1000', u'Show - Everything'),
])


class IMyLibrary(IPortletDataProvider):

    student_guide_link = schema.TextLine(title=_(u"Student Guide Information"),
                                         description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                         required=False,
                                         default=u"Students|${root_url}/community/students")
    student_body_links = schema.List(title=_(u"Student Guide Links"),
                                     description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                     required=False,
                                     value_type = schema.TextLine(title=_(u"Student Guide Links"),
                                                                  description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                                                  )
                                     )
    
    
    
    graduate_guide_link = schema.TextLine(title=_(u"Graduate Guide URL"),
                                         description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                          required=False,
                                          default=u"Graduate & Students|${root_url}/community/graduates")
    graduate_body_links = schema.List(title=_(u"Graduate Guide Links"),
                                     description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                     required=False,
                                     value_type = schema.TextLine(title=_(u"Graduate Guide Links"),
                                                                  description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                                                  )
                                     )
    
    faculty_guide_link = schema.TextLine(title=_(u"Faculty and Staff Guide URL"),
                                         description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                         required=False,
                                         default=u"Faculty & Staff|${root_url}/community/faculty-and-staff")
    faculty_body_links = schema.List(title=_(u"Faculty and Staff Guide Links"),
                                     description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                     required=False,
                                     value_type = schema.TextLine(title=_(u"Faculty and Staff Guide Links"),
                                                                  description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                                                  )
                                     )
    
    visitor_guide_link = schema.TextLine(title=_(u"Visitor and Alumni Guide URL"),
                                         description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                         required=False,
                                         default=u"Alumni & Visitors|${root_url}/community/alumni-and-visitors")
    visitor_body_links = schema.List(title=_(u"Visitor and Alumni Guide Links"),
                                     description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                     required=False,
                                     value_type = schema.TextLine(title=_(u"Visitor and Alumni Guide Links"),
                                                                  description=_(u"Please use format 'Title|URL' per line.  Note: ${root_url} allowed."),
                                                                  )
                                     )
    
    news_limit_aud = schema.Choice(title=_(u"Audience News Items"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=1)
    
    news_limit_sub = schema.Choice(title=_(u"Subject News Items"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=1)
    
    news_timespan = schema.Int(title=_(u"How many days should this news items be visible in this portlet?"),
                               description=_(u"Please specify an integer."), 
                               required=True, 
                               default=90)
    
    journals_limit = schema.Choice(title=_(u"Research Database Links"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=3)
    
    primary_sources_limit = schema.Choice(title=_(u"Book Links (Grouped With Research Database Links)"),
                                           vocabulary=limit_no_heading_vocabulary,
                                           required=True,
                                           default=1)
    
    books_limit = schema.Choice(title=_(u"Primary Source Links (Grouped With Research Database Links)"),
                                   vocabulary=limit_no_heading_vocabulary,
                                   required=True,
                                   default=1)
    
    references_limit = schema.Choice(title=_(u"Background and References Links"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=0)
    
    gov_limit = schema.Choice(title=_(u"Government Information Links"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=0)

    emc_limit = schema.Choice(title=_(u"EMC Links"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=0)
    
    arc_limit = schema.Choice(title=_(u"Archives Links"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=0)
    
    campus_resources_limit = schema.Choice(title=_(u"Campus Resource Links"),
                                   vocabulary=limit_vocabulary,
                                   required=True,
                                   default=0)


class Assignment(base.Assignment):
    """ Portlet assignment. This is what is actually managed through the portlets UI and associated with columns. """

    implements(IMyLibrary)

    def __init__(self,**kwargs):
        self.student_guide_link = kwargs.get('student_guide_link','')
        self.student_body_links = kwargs.get('student_body_links','')
        self.graduate_guide_link = kwargs.get('graduate_guide_link','')
        self.graduate_body_links = kwargs.get('graduate_body_links','')
        self.faculty_guide_link = kwargs.get('faculty_guide_link','')
        self.faculty_body_links = kwargs.get('faculty_body_links','')
        self.visitor_guide_link = kwargs.get('visitor_guide_link','')
        self.visitor_body_links = kwargs.get('visitor_body_links','')
        self.news_limit_sub = kwargs.get('news_limit_sub',1)
        self.news_limit_aud = kwargs.get('news_limit_aud',1)
        self.news_timespan = kwargs.get('news_timespan',90)
        self.journals_limit = kwargs.get('journals_limit',3)
        self.primary_sources_limit = kwargs.get('primary_sources_limit',1)
        self.books_limit = kwargs.get('books_limit',1)
        self.references_limit = kwargs.get('references_limit',0)
        self.gov_limit = kwargs.get('gov_limit',0)
        self.emc_limit = kwargs.get('emc_limit',0)
        self.arc_limit = kwargs.get('arc_limit',0)
        self.campus_resources_limit = kwargs.get('campus_resources_limit',0)

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"My Library")


class Renderer(base.Renderer):
    """ View class """

    render = ViewPageTemplateFile('my_library.pt')
    EzProxy = util.EzProxy 
    
    TYPE_STUDENT = 'student'
    TYPE_GRADUATE_STUDENT = 'graduate'
    TYPE_FACULTY_STAFF = 'faculty'
    TYPE_ALUMNI_VISITOR = 'visitor'
    
    books = []
    research_databases = []
    references = []
    primary_sources = []
    campus_resources = []
    voyager_books = []
    voyager_books_ranges = ""
    voyager_books_range_title = ""
    
    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        change = request.form.get('change', False)
        
        if change == "clear":
            self.cookies_purge()
            self.request.response.redirect(self.context.absolute_url())
        elif change == "set" and not self.cookies_exist():
            self.request.response.setCookie("audience", request.form.get("audience",""),path="/")
            self.request.response.setCookie("subject", request.form.get("subject",""),path="/")
            self.request.response.redirect(self.context.absolute_url())
    
    def cookie_history(self, name, check_against):
        try:
            return (check_against == self.request[name])
        except: pass
        return False
        
    def cookies_exist(self):
        return True if self.request.cookies.get("audience", "") != "" else False

    def cookies_purge(self):
        self.request.response.setCookie("past_audience",self.what_audience,path="/")
        self.request.response.setCookie("past_subject",self.what_subject,path="/")
        self.request.response.setCookie("audience","",path="/")
        self.request.response.setCookie("subject","",path="/")

    @property
    def what_subject(self):
        return self.request['subject']
    
    @property
    def what_audience(self):
        return self.request['audience']

    @property
    def get_subject_list(self):
        return getToolByName(self.context, 'portal_catalog').searchResults(portal_type='LibrarySubjectGuide', 
                                                                           path={'query':util.getGuidesPath(self.context)},
                                                                           sort_on='sortable_title', sort_order='ascending')

    @property
    def audience(self):
        data = self._line_formatter(getattr(self.data, self.what_audience + '_guide_link'))
        data['links'] =  self._line_formatter(getattr(self.data, self.what_audience + '_body_links'))

        data['news'] = {'tags': tuple(["Visitors","Alumni"]) , 'path' : 'news' }
        if self.what_audience == self.TYPE_STUDENT:
            data['news'] = {'tags' : 'Students' , 'path' : 'news/topics/Students' }
        elif self.what_audience == self.TYPE_GRADUATE_STUDENT:
            data['news'] = {'tags' : 'Graduate Students' , 'path' : 'news/topics/Graduate Students' }
        elif self.what_audience == self.TYPE_FACULTY_STAFF:
            data['news'] = {'tags' : 'Instructors' , 'path' : 'news/topics/Instructors' }
        
        from_start = DateTime() - self.data.news_timespan
        brains = getToolByName(self.context, 'portal_catalog').searchResults(portal_type='WeblogEntry',
                                                                             Subject=data['news']['tags'],
                                                                             sort_on='created',
                                                                             sort_order='descending',
                                                                             review_state='published',
                                                                             created={'query':(from_start,DateTime('2045-11-19 11:59:00')),
                                                                                               'range': 'min:max'}
                                                                             )
        data['news']['posts'] = brains[:self.data.news_limit_aud]
        return data
    
    @property
    def subject(self):
        data = {}
        brains = getToolByName(self.context, 'portal_catalog').searchResults(portal_type='LibraryCache', path={'query':self.what_subject})
        if brains:
            cache = brains[0].getObject()
            cache_data = cache.getCache()
            data['guide'] = cache.aq_parent
            books = SubjectFactory.parse_cache(2, cache_data, self.data.books_limit)
            research_databases = SubjectFactory.parse_cache(3, cache_data, self.data.journals_limit)
            primary_sources = SubjectFactory.parse_cache(4, cache_data, self.data.primary_sources_limit)
            
            data['research_databases'] = research_databases + books + primary_sources
            data['references'] = SubjectFactory.parse_cache(1, cache_data, self.data.references_limit)
            data['campus_resources'] = SubjectFactory.parse_cache(5, cache_data, self.data.campus_resources_limit)
            data['voyager_books'] = cache_data['voyager']
            data['voyager_books_ranges'] = cache_data['callrange']
            data['voyager_books_range_title'] = cache_data['callrange_description']
            data['emc_links'] = data['guide'].getEMCListContent()[0:self.data.emc_limit]
            data['gov_links'] = data['guide'].getGovernmentListContent()[0:self.data.gov_limit]
            data['arc_links'] = data['guide'].getArchivesListContent()[0:self.data.arc_limit]
            data['news'] = {'tags' : data['guide'].getNewsTopic() , 'path' : 'news/topics/' + data['guide'].getNewsTopic() }
            
            from_start = DateTime() - self.data.news_timespan
            brains = getToolByName(self.context, 'portal_catalog').searchResults(portal_type='WeblogEntry',
                                                                                 Subject=data['news']['tags'],
                                                                                 sort_on='created',
                                                                                 sort_order='descending',
                                                                                 review_state='published',
                                                                                 created={'query':(from_start,DateTime('2045-11-19 11:59:00')),
                                                                                                   'range': 'min:max'}
                                                                                 )
            data['news']['posts'] = brains[:self.data.news_limit_sub]
        return data
        
    def _line_formatter(self, line):
        if isinstance(line, list):
            results = []
            for l in line:
                results.append(self._line_formatter(l))
            return results
        a = line.replace('${root_url}', self.portal_obj.absolute_url()).split('|')
        return {'Title' : a[0],'getURL' : a[1]}

    def shorten_text(self,text,length=23):
        if len(text) < length:
            return text
        else:
            return text[0:length] + "..."
        
    @property
    def portal_obj(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


class AddForm(base.AddForm):
    """ Portlet add form. """
    form_fields = form.Fields(IMyLibrary)

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """ Portlet edit form. """
    form_fields = form.Fields(IMyLibrary)
