"""
project = "Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "2_return_url_json.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/25/2018"
author_email = "patrick@revxcorp.com",
description = ("Step 2 of 3:  Extract, transform, and load data from result.json into a SQLite database needed to maintain traceability and de-duplication of pages returned by study population web servers."),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""

import json
import sqlite3
from urllib.parse import urlsplit

# read JSON Results
dir_name = '_data/2016-10-05T14:51:11.452293/'
file_json = dir_name + 'result.json'
json_string = open(file_json).read()
json_data = json.loads(str(json_string))

# connect to privacy DB
conn = sqlite3.connect('privacydb.sqlite')
cur = conn.cursor()

for call in json_data:

    # read JSON file to update records with Return information
    urlReturn = json_data[call]['pageRedirectEndURL'].strip().lower()
    fileName = json_data[call]['filename'].strip()
    requestUUID = fileName.split('.')[0]
    scheme, host, path, query, fragment = urlsplit(urlReturn)
    urlRootReturn = host + path + query + fragment
    if scheme == 'http':
        digCertReturn = 0
    else:
        digCertReturn = 1

    cur.execute("SELECT id FROM UrlRequest WHERE requestUUID = ?",
                (requestUUID,))
    urlRequestID = cur.fetchone()[0]

    # Insert results record from result.json
    cur.execute('''
      UPDATE UrlRequest
      SET urlReturn = ?,  urlRootReturn = ?, digCertReturn = ?
      WHERE id = ?''',
                (urlReturn, urlRootReturn, digCertReturn, urlRequestID,))

    conn.commit()
