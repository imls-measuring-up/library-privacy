# project = "python"
# name = "test",
# version = "0.1",
# author = "Patrick OBrien",
# date = "$08/28/2016"
# author_email = "patrick@revxcorp.com",
# description = ("xx"),
# license = "LICENSE",
# keywords = "",
# url = "",


import os
import sqlite3
import json
import re
from urllib.parse import urlsplit, urlunsplit


dirName = input('enter data directory (e.g.,2016-08-18T09:49:29.308456): ')
if ( len(dirName) < 1) : dirName = '2016-08-18T09:49:29.308456'
fileJson = dirName + '/result.json'

# read JSON Results
jsonString = open(fileJson).read()
jsonData = json.loads(jsonString)

conn = sqlite3.connect('privacydb.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS Library;

CREATE TABLE IF NOT EXISTS Library (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    parent_id INTEGER ,
    url     TEXT UNIQUE,
    url_type TEXT ,
    redirect  TEXT  ,
    return_type TEXT ,
    return_url TEXT
)
''')


count = 0

for call in jsonData:
    count += 1

    # capture redirects in list
    redirectType = list()
    redirects = (jsonData[call]['pageRedirectHist'])
    redirects = re.findall('([0-9.]+)', redirects)
    # print(count, len(redirectType), redirectType)
    if len(redirects) == 0:
        redirects = 'none'
    else:
        redirects = ','.join(redirects)



    # Get return url and determine type
    returnUrl = jsonData[call]['pageRedirectEndURL']
    returnType = urlsplit(returnUrl)[0]

    # Parse request url into type, host and Parent url for lookup
    urlType = urlsplit(call)[0]
    hostCall = urlsplit(call)[1]

    # Lookup Library parent organization's upper domain
    school = hostCall.rstrip().split('.')
    if len(school[-1]) == 3 or hostCall.endswith('ca') == True:
        url = school[-2] + '.' + school[-1]
    else:
        url = school[-3] + '.' + school[-2] + '.' + school[-1]
        if url.startswith('www') == True:
            url = school[-2] + '.' + school[-1]

    # print(count, url, returnType, returnUrl, redirects)


    cur.execute("SELECT id FROM Parent WHERE url= ?", (url, ))
    parent_id = cur.fetchone()[0]
    # print(count, parent_id, url, urlType, call)
    # print(count, parent_id, url, returnType, returnUrl)


    cur.execute('''INSERT OR IGNORE INTO Library
      (parent_id, url, url_type, redirect, return_type, return_url)
      VALUES ( ?, ?, ?, ?, ?, ? )''',
        (parent_id, call, urlType, redirects, returnType, returnUrl ))


    conn.commit()




