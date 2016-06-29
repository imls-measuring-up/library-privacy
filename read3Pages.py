from lxml import html
import requests
import urllib2
from bs4 import BeautifulSoup

# import urllib, ssl, \

# Define Variables
# Get Member Library Names and URLs
dataDLF = 'https://www.diglib.org/members/'
dataARL = 'http://www.arl.org/membership/list-of-arl-members'
dataOCLC = 'http://www.oclc.org/research/partnership/roster.html'


memberLibrary = 'www.usbank.com'
page = 'http://'+ memberLibrary
pageSecure = 'https://' + memberLibrary  # Does Library Have A Secure Page


print page, pageSecure
# def getHTML(name):
requestPageSecure = requests.get(pageSecure, verify=True)
requestPage = requests.get(page, allow_redirects=True)
pageHTML = requestPage.content
pageHeaders = requestPage.headers
pageCookies = requestPage.cookies
pageRedirectHist = requestPage.history, requestPage.url


soup = BeautifulSoup(pageHTML, 'lxml')
fileNameContent = page.split('/')[2] + '.html'
fileNameHeader = page.split('/')[2] + '.Header.txt'


#     print fileName
#     print textPage
print fileNameContent, fileNameHeader
print pageCookies
print 'Redirect history:', pageRedirectHist
print 'Secure Request: ', requestPageSecure
print 'Page Headers: ', pageHeaders
print 'pageHTML: ', pageHTML
# print soup

# citeDict = dict()
# citeList = list()
#
#
# # Define Functions
#
#
# def getUrl(page):
#     scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
#     uh = urllib.urlopen(page, context=scontext)
#     data = uh.read()
#     soup = BeautifulSoup(data)
#
#     print tags
#     for tag in tags[start: pos]:
#         nextName = tag.contents[0].encode("utf-8")
#         nextUrl = tag.get('href', None).encode("utf-8")
#
#
# def readFile(fname):  # Create Dictionary of Key Value pairs
#
#     # open file
#     fh = open(fname, 'r')
#
#     # convert file into Dictionary
#     for line in fh:
#         key, val = line.split()
#         citeDict[str(key)] = val




        #
        # readFile(dataSet)
        #
        # print 'citeDit ', citeDict
        #
        # # def urlCitation(luDict):
        # for (recordId,luUrl) in citeDict.items():
        #     html = urllib.urlopen(luUrl).read()
        #     soup = BeautifulSoup(html)
        #     citation = soup.find(id="metadata_identia")
        #     # print 'citation= ', citation
        #     x = citation.contents[0].encode("utf-8")
        #     x = x.rstrip()
        #     x = x.lstrip()
        #     print recordId, x
        # citeList.append( (recordId, x))

        #     stuff = tag.contents[0].encode("utf-8")
        #     sumlist.append(stuff)
        #
        # sumlist = map(int, sumlist)
        # print sum(sumlist)
