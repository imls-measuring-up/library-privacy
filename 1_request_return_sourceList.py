# project = "python"
# name = "1_request_return_sourceList.py",
# version = "0.1",
# author =Patrick OBrien",
# date = "08/25/2016"
# author_email = "patrick@revxcorp.com",
# description = ("step 1 of 3 to generate dataset used for running privacy research test on the HTML files of ARL, DLF, and OCLC research libraries.  This script reads log.txt to create a SQLite DB containing teh Unique Parent Institutions (UPI), unique Fully Qualified Domain Names (FQDN), and unique URL requests for each research library.")
# license = "LICENSE",
# keywords = "IMLS, measuring up, research libraries, privacy",
# url = "",

import sqlite3
import csv

from urllib.parse import urlsplit, urlunsplit


# Create SQLite DB
conn = sqlite3.connect('privacydb_json.sqlite')
cur = conn.cursor()


# Create SQLite Tables for Unique Parent Institutions (UPI), unique Fully Qualified Domain Names (FQDN), and unique URL request (URL) from ARL, DLF, and OCLC research libraries

cur.executescript('''

DROP TABLE IF EXISTS Parents; -- unique parent institution Top Level Domains (TLD) (e.g., montana.edu == Montana State University)
DROP TABLE IF EXISTS Hosts; -- unique FQDN published by ARL, DLF and OCLC on membership webpages
DROP TABLE IF EXISTS Names; -- names published with URLs by ARL, DLF, and OCLC
DROP TABLE IF EXISTS Urls;  -- unique URLs published by ARL, DLF and OCLC membership web pages.

-- table containing UPI TLD and country
CREATE TABLE IF NOT EXISTS Parents (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    hostParent   TEXT UNIQUE,
    country  TEXT
);

-- table containing all the FQDN of research libraries
CREATE TABLE IF NOT EXISTS Hosts (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    hostLib TEXT UNIQUE ,
    parentID INTEGER
);

CREATE TABLE IF NOT EXISTS Names (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    nameSchool TEXT ,
    membership TEXT,
    parentID  INTEGER ,
    hostID  INTEGER
);


-- table of URL request and returns (log.txt)
CREATE TABLE IF NOT EXISTS URLs (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    -- requestNo  INTEGER UNIQUE ,
    urlRequest TEXT UNIQUE,
    parentID INTEGER ,
    hostID INTEGER ,  --libraryID
    sourceList INTEGER, -- 1 = Yes 0 == No
    sourceUUID TEXT ,
    urlRootRequest TEXT ,
    digCertRequest INTEGER   -- 1 = Yes 0 == No
)



''')


# read log.txt file
dirName = input('enter data directory (e.g.,2016-08-18T09:49:29.308456): ')
if len(dirName) < 1: dirName = '2016-10-05T14:51:11.452293'


data_file = dirName + '/sourceList.txt'

print(data_file)

with open(data_file, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)

    count = 0

    for row in reader:
        print(row)
        timeStamp = row['timestamp']
        sourceUUID = row['sourceUUID'].strip()
        membership = row['membership'].strip().lower()
        nameSchool = row['school'].strip().lower()
        urlRequest = row['url'].strip().lower()
        membership = membership.split('.')[1].upper()
        sourceList = 1

        # parse requested URL into components
        scheme, host, path, query, fragment = urlsplit(urlRequest)
        hostLib = host
        urlRootRequest = host + path + query + fragment

        # determine if the requested url has a secure digital cert (https:\\) or not (http:\\)
        if scheme == 'http':
            digCertRequest = 0
        else:
            digCertRequest = 1

        school = host.split('.')

        # Identify unique PI Top Level Domain (TLD) & country
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
        if hostParent == 'bibalex.org': country = 'eg'
        if hostParent == 'aucegypt.edu': country = 'eg'
        if hostParent == 'huc.edu': country = 'il'
        if hostParent == 'leiden.edu': country = 'nl'

        # Insert unique PI and country
        cur.execute('''INSERT OR IGNORE INTO Parents (hostParent, country)
            VALUES ( ?, ? )''', (hostParent, country,))

        # Use a research library FQDN to lookup primary key of ressearch library's PI
        cur.execute('SELECT id FROM Parents WHERE hostParent = ? ', (hostParent,))
        parentID = cur.fetchone()[0]

        # Insert unique FQDN's used by research libraries
        cur.execute('''INSERT OR IGNORE INTO Hosts (hostLib, parentID)
            VALUES ( ?, ? )''', (hostLib, parentID,))

        # lookup primary key of research library FQDN
        cur.execute('SELECT id FROM Hosts WHERE hostLib = ? ', (hostLib,))
        hostID = cur.fetchone()[0]

        # Insert research library names published by membership
        cur.execute('''INSERT OR IGNORE INTO Names (nameSchool, membership,
            parentID, hostID )
            VALUES ( ?, ?, ?, ? )''', ( nameSchool, membership, parentID, hostLib, ))

        # Insert URL request data (count = 860)
        cur.execute('''INSERT OR IGNORE INTO URLs
            (urlRequest, parentID, hostID, sourceList, sourceUUID,
            urlRootRequest, digCertRequest )
            VALUES ( ?, ?, ?, ?, ?, ?, ? )''',
            (urlRequest, parentID, hostID, sourceList, sourceUUID,
            urlRootRequest, digCertRequest ))

    # write SQLite DB used for analysis
    conn.commit()

