"""
project = "Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "data2_membership_list.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/25/2018"
author_email = "patrick@revxcorp.com",
description = ("Extract research library URLs from DLF, ARL, and OCLC research library membership HTML pages"),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""

import csv
import re

from bs4 import BeautifulSoup

# set variables
organizations = ['www.arl.org', 'www.diglib.org', 'www.oclc.org']
data_directory = '_data/membership/'
file_name = data_directory + 'data_all_library.csv'


# open the research library membership HTML files
def open_html_file(name):
    open_html_file.data = open(data_directory + name + '.html')  # open membership HTML page
    open_html_file.domain = org.split('.')[1] + '.' + org.split('.')[
        2]  # parse organization name to exclude internal website links and create filename
    open_html_file.soup = BeautifulSoup(open_html_file.data, 'lxml')  # BeautifulSoup object containing HTML data


# extract and write research library names and URLs to a .CSV file
def get_urls(org, num, tags, check, writer):
    for tag in tags[num].find_all('a'):
        try:
            if tag is not None:
                next_url = tag.get('href', None)
                if not next_url.startswith("http"):
                    continue
                next_name = tag.contents[0]
                test_org = re.findall(check, next_url)
                test_goog = re.findall('google', next_url)
                if len(test_org) + len(test_goog) == 0:
                    print(next_name, next_url)
                    writer.writerow([org, next_name, next_url])
        except Exception as e:
            print
            print("something is wrong with the HTML tag {}: {}".format(tag, e))
            print


with open(file_name, 'w') as toWrite:
    writer = csv.writer(toWrite, delimiter=',')
    writer.writerow(['membership', 'school', 'url'])
    for org in organizations:
        count = 0
        open_html_file(org)
        # find HTML tags encasing Membership data
        if org == organizations[0]:
            tags = open_html_file.soup.find_all('div', class_='article-content')  # ARL
        elif org == organizations[1]:
            tags = open_html_file.soup.find_all('div', class_=re.compile('one_half'))  # DLF
        else:
            tags = open_html_file.soup.find_all('div', class_='text parbase section')  # OCLC
        for i in tags:
            get_urls(org, count, tags, open_html_file.domain, writer)
            count += 1
