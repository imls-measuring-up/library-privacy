"""
project = "Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "data2_membership_list.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/30/2018"
author_email = "patrick@revxcorp.com",
description = ("Extract research library URLs from DLF, ARL, and OCLC research library membership HTML pages"),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""

import csv
import os
import re

from bs4 import BeautifulSoup


def pick_dataset(dir_timestamp):
    os.chdir(os.path.dirname(__file__))  # change dir to current python script location
    write_path = os.path.join(os.getcwd(), '_data/membership/')  # folder for project data
    write_file = os.path.join(os.getcwd(),
                              write_path + 'data_all_library_' + dir_timestamp + '.csv')  # folder for project data
    read_path = os.path.join(os.getcwd(), write_path + dir_timestamp)  # folder for data type

    print("Files will be written to: {}".format(write_path))
    print("Files are read from: {}".format(read_path))
    print('New dataset file: {}'.format(write_file))
    return write_path, read_path, write_file


# open the research library membership HTML files
def open_html_file(open_file, name):
    open_html_file.data = open(open_file + '/' + name + '.html')  # open membership HTML page
    open_html_file.domain = organization.split('.')[1] + '.' + organization.split('.')[
        2]  # parse organization name to exclude internal website links and create filename
    open_html_file.soup = BeautifulSoup(open_html_file.data, 'lxml')  # BeautifulSoup object containing HTML data


# extract and write research library names and URLs to a .CSV file
def get_urls(organization, num, tags, check, writer):
    count_member = 0
    for tag in tags[num].find_all('a'):
        try:
            if tag is not None:
                next_url = tag.get('href', None)
                if not next_url.startswith("http"):
                    continue
                test_org = re.findall(check, next_url)
                test_goog = re.findall('google', next_url)
                if 'webjunction' in next_url:
                    break
                if 'hangingtogether' in next_url:
                    break
                if len(test_org) + len(test_goog) == 0:
                    next_name = tag.contents[0].strip(",")
                    count_member += 1
                    next_name = next_name.replace(',', '')
                    print('{} member {} -  {} @ {}'.format(organization, count_member, next_name, next_url))
                    writer.writerow([organization, next_name, next_url])
        except Exception as e:
            print
            print("something is wrong with the HTML tag {}: {}".format(tag, e))
            print


# list the membership organization urls
organizations = ['www.arl.org', 'www.diglib.org', 'www.oclc.org']

# set read / write path and file names
write_path, read_path, write_file = pick_dataset('2018-07-30T15_45_32.751109')

with open(write_file, 'w') as toWrite:
    writer = csv.writer(toWrite, delimiter=',')
    writer.writerow(['membership', 'school', 'url'])
    for organization in organizations:
        count = 0
        open_html_file(read_path, organization)
        # find HTML tags encasing Membership data
        if organization == organizations[0]:
            tags = open_html_file.soup.find_all('div', class_='article-content')  # ARL
        elif organization == organizations[1]:
            tags = open_html_file.soup.find_all('div', class_=re.compile('entry-content'))  # DLF
        else:
            tags = open_html_file.soup.find_all('div', class_='text parbase section')  # OCLC
        for i in tags:
            get_urls(organization, count, tags, open_html_file.domain, writer)
            count += 1
