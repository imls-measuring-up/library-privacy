from bs4 import BeautifulSoup
import re, os, csv

# set variables
# orgs = {'www.arl.org': "class_='article-content'", 'www.diglib.org': "class_=re.compile('one_half')", 'www.oclc.org': "class_='text parbase section'"}
orgs = ['www.arl.org', 'www.diglib.org', 'www.oclc.org']




def openHtmlFile(name):
    openHtmlFile.data = open(name + '.html') # open membership HTML page
    openHtmlFile.domain = org.split('.')[1] + '.' + org.split('.')[2] # parse organization name to exclude internal website links and create filename
    openHtmlFile.soup = BeautifulSoup(openHtmlFile.data, 'lxml') # BeautifulSoup object containing HTML data
    # for key, value in orgs.iteritems():
    #     tags = openHtmlFile.soup.find_all('div', lookFor)
    #     with open('data_' + openHtmlFile.domain + '.csv', 'w') as toWriteMember:
    #         memWriter = csv.writer(toWriteMember, delimiter=',')
    #         memWriter.writerow(['school', 'url'])

    #return (openHtmlFile.domain, openHtmlFile.soup)


def getUrls(org, num, tags, check, writer):
    for tag in tags[num].find_all('a'):
        try:
            if tag is not None:
                nextUrl = tag.get('href', None).encode("utf-8")
                if not nextUrl.startswith("http") : continue
                nextName = tag.contents[0].encode("utf-8")
                testOrg = re.findall(check, nextUrl)
                testGoog = re.findall('google', nextUrl)
                if len(testOrg) + len(testGoog) == 0:
                    print nextName, nextUrl
                    writer.writerow([org, nextName, nextUrl])
                    # memWriter.writerow([nextName, nextUrl])
        except:
           # print 'item', num, item
           continue



with open('data_all_library.csv', 'w') as toWrite:
    writer = csv.writer(toWrite, delimiter=',')
    writer.writerow(['membership', 'school', 'url'])
    for org in orgs:
        count = 0
        openHtmlFile(org)
            # find HTML tags encasing Membership data
        if org == orgs[0]:
            tags = openHtmlFile.soup.find_all('div', class_='article-content') #ARL
        elif org == orgs[1]:
            tags = openHtmlFile.soup.find_all('div', class_=re.compile('one_half')) # DLF
        else:
            tags = openHtmlFile.soup.find_all('div', class_='text parbase section') #OCLC
        for i in tags:
            getUrls(org, count, tags, openHtmlFile.domain, writer)
            count +=1
