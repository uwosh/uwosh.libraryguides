from Products.CMFCore.utils import getToolByName
from xml.dom import minidom
import cookielib, urllib2
import socket
import logging
logger = logging.getLogger("Plone")

class VoyagerDAO:
    """
    Connects to the VoyagersDB's Webservices and returns results in XML format.
    There is a formatter to transfer the XML data into python objects.
    @author: David Hietpas
    @version: 1.0
    """
    xmldoc = None
    DEFAULT_TIMEOUT_SECONDS = 30
    
    def __init__(self):
        """
        Initializes the Voyager Session for handling requests.
        """
        self.session = self._createCookieHandler()
    """
    Creates the Cookie for handling the session.
    """
    def _createCookieHandler(self):
        cj = cookielib.CookieJar()
        socket.setdefaulttimeout(self.DEFAULT_TIMEOUT_SECONDS)
        return urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    
    def _getVoyagerUrl(self):
        props = getToolByName(self, 'portal_properties')
        return props.external_resources.getProperty('voyager_xml_over_http')

    def voyagerSearchService(self,searchCode="GKEY",searchArg=None,maxResultsPerPage="10",searchArgType="AND",displayRelevanceFlag="N"):
        """
        Voyagers SearchService
        @param searchCode: Code Constraint to search on.
        @param searchArg: Item('s) to be searched. 
        @param maxResultsPerPage: Number of results returned
        @param searchArgType: How to connect your searchArgs aka AND or OR  
        @param displayRelevanceFlag:  Is Browse?  Y|N
        @return: xml
        """
        self.xmldoc = None
        if searchArg != None:
            query = ("searchCode=" + searchCode + 
                     "&searchArg=" + searchArg + 
                     "&maxResultsPerPage=" + maxResultsPerPage + 
                     "&searchArgType=" + searchArgType + 
                     "&displayRelevanceFlag=" + displayRelevanceFlag)
            try:
                print str(self._getVoyagerUrl()) + "/SearchService?" + query
                socket = self.session.open(str(self._getVoyagerUrl()) + "/SearchService?" + query,timeout=self.DEFAULT_TIMEOUT_SECONDS)
                self.xmldoc = minidom.parse(socket).documentElement
                socket.close()
            except Exception as e:
                logger.warning(e)
            #print self.xmldoc.toprettyxml(encoding='utf-8')
        return self.xmldoc
    
    def voyagerSearchResultsService(self,searchType=None,resultPointer="0",maxResultsPerPage="10",sortBy="TITLE",profileCode=None):
        """
        Voyagers SearchResultsService
        @param searchType: FIND,BROWSE,etc
        @param resultPointer: Current position in result set.
        @param maxResultsPerPage: Number of results returned
        @param sortBy: Field to sort on. 
        @param profileCode: Ignore, used only one RELBIBS
        @return: xml
        """
        self.xmldoc = None
        if searchType != None:
            query = ("searchType=" + searchType + 
                     "&resultPointer=" + resultPointer + 
                     "&maxResultsPerPage=" + maxResultsPerPage + 
                     "&sortBy=" + sortBy)
            try:
                print str(self._getVoyagerUrl()) + "/SearchResultsService?" + query
                socket = self.session.open(str(self._getVoyagerUrl()) + "/SearchResultsService?" + query,timeout=self.DEFAULT_TIMEOUT_SECONDS)
                self.xmldoc = minidom.parse(socket).documentElement
                socket.close()
            except Exception as e:
                logger.warning(e)
            #print self.xmldoc.toprettyxml(encoding='utf-8')
        return self.xmldoc

    def xmlToList(self,xml=None):
        """
        Formats Voyagers SearchServices XML response into a python List[] of python Objects{}.
        @param xml: Voyagers XML response, if not provided this will use the last received xml.
        @return: []: Returns a List of Python Objects.
        """
        results = []
        response = []
        
        
        #self._dump_xml(xml)
        #print xml.toprettyxml( encoding='utf-8')
        
        if xml == None:
            xml = self.xmldoc
        try:
            results = xml.getElementsByTagName('sear:result')
        except Exception as e:
            logger.error(e)
            
        for result in results:
            obj = {}
            obj['bibId'] = self._getText(result.getElementsByTagName("sear:bibId"))
            obj['title'] = self._getText(result.getElementsByTagName("sear:bibText1"))
            obj['title_clean'] = self._cleanTitle(self._getText(result.getElementsByTagName("sear:bibText1")))
            obj['author'] = self._getText(result.getElementsByTagName("sear:bibText2"))
            obj['author'] = self._getText(result.getElementsByTagName("sear:bibText2"))
            obj['pubDate'] = self._getText(result.getElementsByTagName("sear:bibText3"))
            obj['callnumber'] = self._getText(result.getElementsByTagName("sear:callNumber"))
            obj['location'] = self._getText(result.getElementsByTagName("sear:locationName"))
            obj['itemCount'] = self._getText(result.getElementsByTagName("sear:itemCount"))
            obj['itemStatus'] = self._getText(result.getElementsByTagName("sear:itemStatusCode"))
            obj['issn'] = self._getText(result.getElementsByTagName("sear:issn"))
            obj['isbn'] = self._getText(result.getElementsByTagName("sear:isbn"))
            obj['google_bib'] = "ISBN:" + self._getText(result.getElementsByTagName("sear:isbn"))
            
            """ FIX: There is a bug in Voyager 8 with isbn and issn being swapped, this is a simple fix for the time being. """
            if obj['isbn'] == "":
                obj['isbn'] = obj['issn'] 
            """ END FIX: There is a bug in Voyager 8 with isbn and issn being swapped, this is a simple fix for the time being. """
            
            #print str(obj)
            #print ""
            response.append(obj)
        
        
        return response
    

    def _dump_xml(self,xml):
        f = open('C:\Users\hietpasd\Desktop\call.txt', 'w')
        f.write(xml.toprettyxml( encoding='utf-8'))
        print "Outputing"
        
    def _getText(self,tag):
        if len(tag) != 0:
            if len(tag[0].childNodes) != 0:
                return tag[0].childNodes[0].data
        return ""

    def _cleanTitle(self,text):
        return text.split("/")[0]



    def testConnection(self):
        self.voyagerSearchService(searchArg="foo")
        results = self.xmlToList(xml=self.voyagerSearchResultsService(searchType="FIND",maxResultsPerPage="1"))
        if results != None:
            if len(results) > 0:
                return True
            return False
        return False

    #OLD OUT DATED
    def fakeXML(self):
        fakecontent = str('<results>'+
             '<result>'+
                  '<bibId>399653</bibId>'+
                  '<bibText1>Permian-Triassic Pangean basins. / Veevers, J. J.</bibText1>'+
                  '<bibText2>Veevers, J. J.</bibText2>'+
                  '<bibText3>1989</bibText3>'+
                  '<callNumber>ND212 .A148 1989</callNumber>'+
                  '<mfhdCount>1</mfhdCount>'+
                  '<itemCount>1</itemCount>'+
                  '<itemStatusCode>1</itemStatusCode>'+
                  '<patronGroupCode/>'+
                  '<locationName>Medical Lib:Main Collection</locationName>'+
                  '<opacSuppressFlag>N</opacSuppressFlag>'+
                  '<relevanceRanking/>'+
                  '<headingText />'+
                  '<headingType />'+
                  '<indexCode />'+
                  '<databaseCode />'+
                  '<elink />'+
                  '<elinkType  />'+
                  '<isbn>0813711843</isbn>'+
                  '<issn />'+
                  '<bibFormat>am</bibFormat>'+
              '</result>' +
             '<result>'+
                  '<bibId>454631</bibId>'+
                  '<bibText1>The nature of magmatism in the Appalachian orogen / John P. Hogan</bibText1>'+
                  '<bibText2>John P. Hogan</bibText2>'+
                  '<bibText3>1919</bibText3>'+
                  '<callNumber>ND212 .A348 1919</callNumber>'+
                  '<mfhdCount>1</mfhdCount>'+
                  '<itemCount>1</itemCount>'+
                  '<itemStatusCode>1</itemStatusCode>'+
                  '<patronGroupCode />'+
                  '<locationName>Medical Lib:Main Collection</locationName>'+
                  '<opacSuppressFlag>N</opacSuppressFlag>'+
                  '<relevanceRanking  />'+
                  '<headingText />'+
                  '<headingType />'+
                  '<indexCode />'+
                  '<databaseCode />'+
                  '<elink />'+
                  '<elinkType  />'+
                  '<isbn>0813711916</isbn>'+
                  '<issn />'+
                  '<bibFormat>am</bibFormat>'+
              '</result>' +
              '<result>'+
                  '<bibId>278709</bibId>'+
                  '<bibText1>Great Basin Lower Devonian Brachiopoda / J. G. Johnson.</bibText1>'+
                  '<bibText2>J. G. Johnson.</bibText2>'+
                  '<bibText3>1911</bibText3>'+
                  '<callNumber>ND212 .A348 1919</callNumber>'+
                  '<mfhdCount>1</mfhdCount>'+
                  '<itemCount>1</itemCount>'+
                  '<itemStatusCode>1</itemStatusCode>'+
                  '<patronGroupCode />'+
                  '<locationName>Medical Lib:Main Collection</locationName>'+
                  '<opacSuppressFlag>N</opacSuppressFlag>'+
                  '<relevanceRanking  />'+
                  '<headingText />'+
                  '<headingType />'+
                  '<indexCode />'+
                  '<databaseCode />'+
                  '<elink />'+
                  '<elinkType  />'+
                  '<isbn>0813711215</isbn>'+
                  '<issn />'+
                  '<bibFormat>am</bibFormat>'+
              '</result>' +
            '</results>'
        )
        return minidom.parseString(fakecontent)
















    