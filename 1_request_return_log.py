"""
project = "Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites"
name = "1_request_return_log.py",
version = "1.0",
author = "Patrick OBrien",
date = "07/25/2018"
author_email = "patrick@revxcorp.com",
description = ("Step 1 of 3:  Extract, transform, and load data from log.txt into a SQLite database to maintain traceability and de-duplication of pages returned by study population web servers needed to perform analysis"),
license = "[MIT license](https://opensource.org/licenses/mit-license.php)",
keywords = "IMLS Measuring Up, Digital Repositories, Research Library Privacy",
url = "https://github.com/imls-measuring-up/library-privacy",
"""

import csv
import sqlite3

from urllib.parse import urlsplit

conn = sqlite3.connect('privacydb.sqlite')
cur = conn.cursor()

# Create SQLite Tables for Unique Parent Institutions (UPI), unique Fully Qualified Domain Names (FQDN), and other data necessary for analysis of the ARL, DLF, and OCLC research libraries

cur.executescript('''

DROP TABLE IF EXISTS Parent;  -- unique parent institution Top Level Domains (TLD) (e.g., montana.edu == Montana State University)
DROP TABLE IF EXISTS Library;  -- unique FQDN published by ARL, DLF and OCLC on membership pages
DROP TABLE IF EXISTS UrlRequest; -- consolidated data necessary for traceability and de-duplication of URLs published, requested, and pages returned by study population web servers.


-- table of Library parent host and country
CREATE TABLE IF NOT EXISTS Parent (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    hostParent   TEXT UNIQUE,
    country  TEXT
);

-- table for library hosts & names
CREATE TABLE IF NOT EXISTS Library (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    hostLib TEXT UNIQUE,
    name   TEXT
);

-- table of URL request and returns (log.txt)
CREATE TABLE IF NOT EXISTS UrlRequest (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    requestNo INTEGER UNIQUE,
    listSequenceNo INTEGER ,
    libraryID INTEGER ,
    parentID INTEGER ,
    sourceUUID TEXT ,
    requestUUID TEXT UNIQUE ,
    urlRequest TEXT ,
    urlRootRequest TEXT ,
    digCertRequest INTEGER ,
    urlReturn TEXT ,
    urlRootReturn TEXT ,
    digCertReturn INTEGER ,
    redirect TEXT ,
    status TEXT ,
    error  TEXT
)



''')

# set variables for working direction and file
dirName = '_data/2016-10-05T14:51:11.452293/'
data_file = dirName + 'log.txt'

with open(data_file, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

    count = 0

    for row in reader:
        # identify unique library urls from organization membership pages
        requestNo = row['requestNo']
        listSequenceNo = row['listSequenceNo']
        urlRequest = row['requestURL'].strip().lower()
        scheme, host, path, query, fragment = urlsplit(urlRequest)
        hostLib = host
        sourceUUID = row['sourceUUID'].strip()
        requestUUID = row['requestUUID'].strip()
        redirect = row['redirects'].strip()
        status = row['status'].strip()
        error = row['error'].strip()

        # determine if the requested url has a secure digital cert (https:\\) or not (http:\\)
        if scheme == 'http':
            digCertRequest = 0
        else:
            digCertRequest = 1

        # Identify Library parent organization's upper domain & country
        urlRootRequest = host + path + query + fragment
        school = host.split('.')
        if len(school[-1]) == 3:
            hostParent = school[-2] + '.' + school[-1]
            country = 'us'
        elif host.endswith('ca'):
            hostParent = school[-2] + '.' + school[-1]
            country = school[-1]
        else:
            hostParent = school[-3] + '.' + school[-2] + '.' + school[-1]
            country = school[-1]
            if hostParent.startswith('ww'):
                hostParent = school[-2] + '.' + school[-1]
        if hostParent == 'bibalex.org':
            country = 'eg'
        if hostParent == 'aucegypt.edu':
            country = 'eg'
        if hostParent == 'huc.edu':
            country = 'il'
        if hostParent == 'leiden.edu':
            country = 'nl'

        # Insert library's parent organization and country
        cur.execute('''INSERT OR IGNORE INTO Parent (hostParent, country)
            VALUES ( ?, ? )''', (hostParent, country,))

        # lookup primary key of library's parent organization
        cur.execute('SELECT id FROM Parent WHERE hostParent = ? ', (hostParent,))
        parentID = cur.fetchone()[0]

        # Insert library host name
        cur.execute('''INSERT OR IGNORE INTO Library (hostLib)
            VALUES ( ? )''', (hostLib,))

        # lookup primary key of library host name
        cur.execute('SELECT id FROM Library WHERE hostLib = ? ', (hostLib,))
        libraryID = cur.fetchone()[0]

        # Insert request data (count = 860)
        cur.execute('''INSERT OR IGNORE INTO UrlRequest
            (requestNo, listSequenceNo, libraryID, parentID, sourceUUID, requestUUID, urlRequest,
            urlRootRequest, digCertRequest, redirect, status, error)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''',
                    (requestNo, listSequenceNo, libraryID, parentID, sourceUUID, requestUUID, urlRequest,
                     urlRootRequest, digCertRequest, redirect, status, error,))

    conn.commit()
