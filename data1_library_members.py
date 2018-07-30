"""
project = "Protecting Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "data1_library_members.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/30/2018"
author_email = "patrick@revxcorp.com",
description = ("Scrape HTML of DLF, ARL, and OCLC research library membership pages."),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""

import csv
import datetime
import os

import requests

# Research library membership names and URLs
data_DLF = 'www.diglib.org/about/members/'
data_ARL = 'www.arl.org/membership/list-of-arl-members'
data_OCLC = 'www.oclc.org/research/partnership/roster.html'
library_list = [data_ARL, data_DLF, data_OCLC]


# Establish directory for saving data files
def set_file_path(write_path):
    os.chdir(os.path.dirname(__file__))  # change dir to current python script location
    write_path_data = os.path.join(os.getcwd(), '_data/')  # folder for project data
    write_path_working = os.path.join(os.getcwd(), write_path_data + write_path)  # folder for data type
    run_time = datetime.datetime.now().isoformat().replace(":", "_")  # time script is run
    write_path = os.path.join(os.getcwd(), write_path_working + '/' + run_time)  # folder for storing data

    # Ensure directory structure exists
    if not os.path.isdir(write_path_data):
        os.mkdir(write_path_data)
    if not os.path.isdir(write_path_working):
        os.mkdir(write_path_working)
    if not os.path.isdir(write_path):
        os.mkdir(write_path)

    print("Files will be written to: {}".format(write_path))
    return write_path


def read_input_file(file_input):
    with open(file_input, 'r') as f:
        read_line = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        return read_line


# function to create file of the DLF, ARL, and OCLC membership web pages
def web_page(read_data, write_path):
    write_path_file = set_file_path(write_path)
    try:
        for member in read_data:
            page = 'http://' + member
            print('calling URL: {}'.format(page))
            request_page = requests.get(page, allow_redirects=True, headers=header)
            page_html = request_page.content
            write_file_name = write_path_file + '/' + member.split('/')[0] + '.html'
            print('saving: {}'.format(write_file_name.split('/')[-1]))
            f = open(write_file_name, 'wb', 1)
            f.write(page_html)
            f.close()
    except Exception as e:
        print()
        print('something when wrong: {}'.format(e))
        print()


#
header = {'user-agent': 'privacy-research'}  # identify purpose of call
web_page(read_data=library_list, write_path='membership')
