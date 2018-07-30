# Protecting Patron Privacy on the Web

"Protecting Patron Privacy on the Web: A Study of HTTPS and Google Analytics Implementation in Academic Library Websites" is one of the products of a research titled [Measuring Up: Assessing Accuracy of Reported Use and Impact of Digital Repositories.](http://scholarworks.montana.edu/xmlui/handle/1/8924)" It was funded by the [Institute of Museum and Library Services (IMLS)](https://www.imls.gov/).

> [Patrick OBrien](https://www.linkedin.com/in/obrienpatricks/), Scott W. H. Young, Kenning Arlitsch, and Karl Benedict. (Accepted) “Protecting Privacy on the Web: A Study of HTTPS and Google Analytics on Academic Library Websites.” Online Information Review - Manuscript ID OIR-02-2018-0056, Publication Pending


## Summary

This repository contains the tools and data necessary for conducting the analysis contained within the paper.  This includes the following:
* Python scripts for the extraction, transformation, and loading of data needed for the final analysis presented
* Membership HTML pages from the three organization used to define the study population
* The research library HTML homepages used for the study


## Python Scripts
1. `data1_library_members.py` - Scrape HTML of DLF, ARL, and OCLC research library membership pages.
2. `data2_membership_list.py` - Extract research library URLs from membership page's HTML.
3. `Privacy Test Notebook.ipynb` - Calls research library homepage URLs published by DLF, ARL, and OCLC and saves the HTML and data returned by research library web servers. 
4. `Extract Distinct HTML File List.ipynb` - Includes a unique identifer needed for traceability and de-dup of final HTML web pages returned.
5. `1_request_return_log.py` - Step 1 of 3:  Extract, transform, and load data from log.txt into a SQLite database to maintain traceability and de-duplication of pages returned by study population web servers needed to perform analysis
6. `2_return_url_json.py` - Step 2 of 3:  Extract, transform, and load data from result.json into a SQLite database needed to maintain traceability and de-duplication of pages returned by study population web servers.
1. `3_unique-uuid.py` - Step 3 of 3:  Identify and rename unique HTML pages for analysis.
1. `4_test_google_privacy.py` - Audit tests for unique research library home pages returned by the study population web servers.



## Raw Data
1. `_data/membership.zip` - Study population defined by DLF, ARL, and OCLC membership.
1. `_data/2016-10-05T14:51:11.452293.zip` - HTML home pages returned by the web servers of study population.
1. `_data/analysis.zip` - Unique HTML pages used for privacy hypothesis testing of the study population.
    * `_data/analysis/unique-request-uuid.txt` - **NOTE:** this file was generated from exporting the SQL database table `UrlRequests` to `privacydb_log_UrlRequest.csv` and using excel to wrangling the data into a schema crosswalk of files returned by study population web servers and unique HTML files used for hypothesis testing.
1. `results.zip` - Unique HTML home pages that tested positive for Google Analytics and Tag Manager.



## License
The content of this project itself is licensed under the [Creative Commons Attribution 4.0 International license](https://creativecommons.org/licenses/by/4.0/), and the underlying source code used to generate and analyze that content is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php).
