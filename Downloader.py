import time
import json
import requests
import os
import zipfile
from selenium import webdriver
from urllib.parse import unquote

from config import make_webdriver


# Retrieves all information about a course from the API
def get_all_info(sleep_amount=1):
    """
    :param sleep_amount: The amount of time to sleep in between requests, to be nice to
                         the server, in seconds.
    
    This function retrieves the metadata for each course listing in SMMDB.
    """
    driver = make_webdriver()
    all_info_list = []
    start = 0
    while True:
        increment = 100
        driver.get("https://smmdb.net/api/getcourses?limit={}&start={}&prettify=1".format(increment, start))
        time.sleep(1)
        pre = driver.find_element_by_tag_name("pre").text
        data = json.loads(pre)
        for datum in data:
            yield datum
        start += 100


def get_id():
    # Selenium starts here, set the capabilities of chrome
    driver = make_webdriver()
    id_list = []
    start = 0
    while True:
        increment = 100
        driver.get("https://smmdb.net/api/getcourses?limit={}&start={}&prettify=1".format(increment, start))
        pre = driver.find_element_by_tag_name("pre").text
        data = json.loads(pre)
        if len(data) == 0:
            return id_list
        else:
            for datum in data:
                id_list.append(datum["id"])
        start += 100


# Downloads a course using the id
def download_via_id(course_id):
    """
    :param course_id: The id of the course which we're downloading.
                      An example would be 5ed81e4f43c8fe3c0786ac87
    Downloads the zipped course from the database, and unzips it.
    """
    course_loc = f'courses/{course_id}'
    if not os.path.isdir(course_loc):
        os.mkdir(course_loc)

    if not os.path.isdir(os.path.join(course_loc, 'course000')):
        url = f'https://smmdb.net/api/downloadcourse?id={course_id}&type=zip'
        req = requests.get(url)
        time.sleep(1)
        
        zip_loc = os.path.join(course_loc, 'course.zip')
        f = open(zip_loc, 'wb')
        f.write(req.content)
        f.close()

        try:
            zip_f = zipfile.ZipFile(zip_loc, 'r')
            zip_f.extractall(course_loc)
            zip_f.close()
        except zipfile.BadZipFile:
            print('failed, skipping...')
        os.remove(zip_loc)
