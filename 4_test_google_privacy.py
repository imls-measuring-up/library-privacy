"""
project = "Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "4_test_google_privacy.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/25/2018"
author_email = "patrick@revxcorp.com",
description = ("Audit tests for unique research library home pages returned by the study population web servers."),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""


import codecs
import csv

# create Org, School, Library and Member
dir_name = '_data/analysis/'
data_file = dir_name + 'unique-request-uuid.txt'
file = 0

with open(data_file, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    count_us, count_uk, count_ca, count_int, count_except = 0, 0, 0, 0, 0

    # unique text used to determine the use of Google Analytics (GA) and Tag Manager
    testing = ['google-analytics.com', 'analytics.js', 'ga.js', 'googletagmanager', 'gtm.js']  # GA & Tag Manager
    # testing = ['anonymizeip',]  # GA IP anonymizer
    # testing = ['forcessl',]  # GA SSL

    for row in reader:
        old_name = row['Request_UUID']
        new_name = row['fileRename']
        test_file = dir_name + new_name + '.html'
        file += 1
        google_true = 0
        country = new_name.split('-')[0]

        with codecs.open(test_file, 'r') as fh:
            try:
                line_num = 0
                for line in fh:
                    if google_true > 0:
                        break
                    check = line.lower().strip()
                    line_num += 1
                    for test in testing:
                        if test in check:
                            if country == 'us':
                                count_us += 1
                            if country == 'ca':
                                count_ca += 1
                            if country == 'uk':
                                count_uk += 1
                            if country == 'International':
                                count_int += 1
                            print('file {} line {} positive {} '.format(file, line_num, new_name))
                            google_true += 1
                            break

                else:
                    continue
            except:
                print("syntax error {} {} {}".format(file, new_name, old_name))
                count_except += 1

    print('us', count_us)
    print('ca', count_ca)
    print('uk', count_uk)
    print('int', count_int)
    print('exceptions', count_except)
