"""
project = "Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "3_unique-uuid.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/25/2018"
author_email = "patrick@revxcorp.com",
description = ("Step 3 of 3:  Identify and rename unique HTML pages for analysis."),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""

import csv
import os

# create Org, School, Library and Member
dir_html = '_data/2016-10-05T14:51:11.452293/'
dir_analysis = '_data/analysis/'
file_input = dir_analysis + 'unique-request-uuid.txt'
print(file_input)

with open(file_input, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

    for row in reader:
        oldName = dir_html + row['Request_UUID'] + '.html'
        newName = dir_analysis + row['fileRename'] + '.html'
        os.rename(oldName, newName)
