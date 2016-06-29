from lxml import html
from bs4 import BeautifulSoup
import re, os, csv, io, html5lib

# set variables
orgsDict = {
    'www.arl.org': "article-content"}  # , 'www.diglib.org': "class_=re.compile('one_half')", 'www.oclc.org': "text parbase section"}


def openHtml(orgDictKey):
    orgHtmlPage = '/data/' + orgDictKey + '.html'  # open membership HTML page
    if orgDictKey.contains('/'):
        domain = orgDictKey.lowercase.parse('/')[0]
    domain = orgDictKey.lowercase.parse('.')
    drop = ['www']
    domain.remove(drop)
    join(domain)


    if orgDictKey.contains('/'):
            domain = orgDictKey.split('/')[0]
        domain = domain.split('.')
            domain =
            domain = orgDictKey.split('.')[1] + '.' + orgDictKey.split('.')[
                2]  # parse organization name to exclude internal website links and create filename
    soup = BeautifulSoup(open(orgHtmlPage))
    return domain, soup


def openCsvFile(domain, columnHeaders):
    csvOutputFileName = domain + '.csv'
    with open(csvOutputFileName, 'w') as csvOutputFile:
        csvWriter = csv.writer(csvOutputFile, delimiter=',')
        csvWriter.writerow([columnHeaders])
    return csvOutputFileName


def closeCsvFile(fileName):
    fileName.close()


def findSoupClasses(soup, orgDict):
    divClass = orgDict[1]
    divHtml = soup.findAll('div', class_=divClass)
    return divHtml


def findSoupUrls(divHtml):
    for div in divHtml:
        htmlTags = div.find_all('a')
        for tag in htmlTags:
            try:
                if tag is None: continue
                if tag.get('href') is None: continue
                if
                nextUrl = tag.get('href', None) #.encode('utf8')
                if not nextUrl.startswith("http"): continue
                nextName = unicode(tag.contents[0].string)
                # testOrg = re.findall(check, nextUrl)
                testGoog = re.findall('google', nextUrl)
                # if len(testOrg) + len(testGoog) == 0:
                if len(testGoog) == 0:
                    print nextName, nextUrl
                    writer.writerow([domain, nextName, nextUrl])
                    memWriter.writerow([nextName, nextUrl])
            except:  # print 'item', num, item
                continue

                # return (openHtmlFile.domain, openHtmlFile.soup)  # def getUrls(org, num, tags, check, writer, memWriter):


# for tag in tags[num].find_all('a'):
#         try:
#             if tag is not None:
#                 nextUrl = tag.get('href', None).encode("utf-8")
#                 if not nextUrl.startswith("http") : continue
#                 nextName = tag.contents[0].encode("utf-8")
#                 testOrg = re.findall(check, nextUrl)
#                 testGoog = re.findall('google', nextUrl)
#                 if len(testOrg) + len(testGoog) == 0:
#                     print nextName, nextUrl
#                     writer.writerow([org, nextName, nextUrl])
#                     memWriter.writerow([nextName, nextUrl])
#         except:
#            # print 'item', num, item
#            continue

def main():
    with open('data_all_library.csv', 'w') as toWrite:
        writer = csv.writer(toWrite, delimiter=',')
        writer.writerow(['membership', 'school', 'url'])
        for orgLib, soupID in orgs.items():
            count = 0
            openHtmlFile(orgLib, soupID, writer)

            # find HTML tags encasing Membership data
            # if org == orgs[0]:
            #     tags = openHtmlFile.soup.find_all('div', class_='article-content') #ARL
            # elif org == orgs[1]:
            #     tags = openHtmlFile.soup.find_all('div', class_=re.compile('one_half')) # DLF
            # else:
            #     tags = openHtmlFile.soup.find_all('div', class_='text parbase section') #OCLC
            # for i in tags:
            # getUrls(org, count, tags, openHtmlFile.domain, writer, memWriter)
            #     count +=1


if __name__ == "__main__":
    main()
