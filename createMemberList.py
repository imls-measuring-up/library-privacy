# project = "python"
# name = "createMemberList",
# version = "0.1",
# author = "Patrick OBrien",
# date = "08/25/2016"
# author_email = "patrick@revxcorp.com",
# description = (" create a SQLite database of the organization, Libraries
#  and their memberships"),
# license = "LICENSE",
# keywords = "IMLS, measuring up, research libraries, privacy",
# url = "",

import sqlite3
import csv
from urllib.parse import urlsplit



conn = sqlite3.connect('privacydb.sqlite')
cur = conn.cursor()

# Create SQLite Tables for Organizations, Libraries and Memberships

cur.executescript('''

DROP TABLE IF EXISTS Org;
DROP TABLE IF EXISTS Parent;
DROP TABLE IF EXISTS Library;
DROP TABLE IF EXISTS Member;



CREATE TABLE IF NOT EXISTS Org (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE,
    url   TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Parent (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE,
    url   TEXT UNIQUE,
    country  TEXT
);

-- connector table for organization many to many with parent
CREATE TABLE IF NOT EXISTS Member (
    org_id  INTEGER,
    parent_id INTEGER,
    PRIMARY KEY (org_id, parent_id)
)
''')


# create Org, School, Library and Member

dataFile = csv.DictReader(open('data_all_library.csv'))

count = 0
for row in dataFile:
    memUrl = row['membership']
    memName = memUrl.split('.')[1].upper()
    scheme, host, path, query, fragment = urlsplit(row['url'])
    libDomain = host
    libUrl = host + path
    libName = row['school'].encode("utf-8")
    count += 1
    school = libDomain.rstrip().split('.')

    # Identify Library parent organization's upper domain

    if len(school[-1]) == 3:
        sDomain = school[-2] + '.' + school[-1]
        country = 'us'
        # print(count, country, sDomain, libDomain)
    elif libDomain.endswith('ca') == True:
        sDomain = school[-2] + '.' + school[-1]
        country = school[-1]
    else:
        sDomain = school[-3] + '.' + school[-2] + '.' + school[-1]
        country = school[-1]
        if sDomain.startswith('www') == True:
            sDomain = school[-2] + '.' + school[-1]
    if sDomain == 'bibalex.org': country = 'eg'
    if sDomain == 'aucegypt.edu': country = 'eg'
    if sDomain == 'huc.edu': country = 'il'
    if sDomain == 'leiden.edu': country = 'nl'

    # Populate Tables
    cur.execute('''INSERT OR IGNORE INTO Org (name, url)
        VALUES ( ?, ? )''', (memName, memUrl, ))

    # lookup primary key of last insert
    cur.execute('SELECT id FROM Org WHERE name = ? ', (memName,))
    org_id = cur.fetchone()[0]


    cur.execute('''INSERT OR IGNORE INTO Parent (name, url, country )
        VALUES ( ?, ?, ? )''', (libName, sDomain, country, ))
    # lookup primary key of last insert
    cur.execute('SELECT id FROM Parent WHERE url = ? ', (sDomain,))
    parent_id = cur.fetchone()[0]

    # cur.execute('''INSERT OR IGNORE INTO Library (name, url)
    #     VALUES ( ?, ? )''', (libName, libUrl, ))
    # cur.execute('SELECT id FROM Library WHERE url = ? ', (libUrl, ))
    # library_id = cur.fetchone()[0]
    # print(library_id, libUrl)

    cur.execute('''INSERT OR IGNORE INTO Member
        (org_id, parent_id ) VALUES ( ?, ? )''',
                (org_id, parent_id ))

    conn.commit()

