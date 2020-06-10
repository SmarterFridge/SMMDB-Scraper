# SMMDB-SQL-Extension
A program to download .cdt files from smmdb.net, parse them via smm-course-viewer, and then insert into a SQL DB

Main.py uses smm-course-viewer to retrieve a course and insert into Mysql 8 database. Selenium used for automation. 
Unzipper.py and Downloader.py will download and unzip all current smm courses from smmdb.net

Many hardcoded directory paths currently, will be updated to be more user friendly in the future


## How To Run

Before running, ensure that your `chromedriver` is set up properly on your PATH.

These instructions are utilized on a machine running Ubuntu, and as such some surface level tweaks are probably necessary to get this dataset collector to run on other platforms.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 Main.py
```
