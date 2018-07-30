"""
project = "Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "data1_library_members.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/25/2018"
author_email = "patrick@revxcorp.com",
description = ("Scrape HTML of DLF, ARL, and OCLC research library membership pages."),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""

import requests

# Get Member Library Names and URLs
data_DLF = 'www.diglib.org/members/'
data_ARL = 'www.arl.org/membership/list-of-arl-members'
data_OCLC = 'www.oclc.org/research/partnership/roster.html'

library_list = [data_ARL, data_DLF, data_OCLC]

data_dir = '_data/membership/'  # set path to write file


# function to create file of the DLF, ARL, and OCLC membership web pages
def web_page(members):
    for member in members:
        page = 'http://' + member
        print(page)
        request_page = requests.get(page, allow_redirects=True)
        page_html = request_page.content
        file_name_content = data_dir + member.split('/')[0] + '.html'
        print(file_name_content)
        print('page_html: ', page_html[:200])
        f = open(file_name_content, 'w', 1)
        f.write(page_html)
        f.close()


web_page(library_list)
