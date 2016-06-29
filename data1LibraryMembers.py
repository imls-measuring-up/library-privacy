import requests

# Get Member Library Names and URLs
dataDLF = 'www.diglib.org/members/'
dataARL = 'www.arl.org/membership/list-of-arl-members'
dataOCLC = 'www.oclc.org/research/partnership/roster.html'

list = [dataARL, dataDLF, dataOCLC]

# function to create file of the DLF, ARL, and OCLC membership web pages
def webPage(members):
    for member in members:
        page = 'http://'+ member
        print page
        requestPage = requests.get(page, allow_redirects=True)
        pageHTML = requestPage.content
        fileNameContent = member.split('/')[0] + '.html'
        print fileNameContent
        print 'pageHTML: ', pageHTML[:200]
        f = open(fileNameContent, 'w', 1)
        f.write(pageHTML)
        f.close()


webPage(list)
