import os
import time

from config import make_webdriver


def ObjectGrabber(course_data_loc):
    # Selenium starts here, set the capabilities of chrome
    driver = make_webdriver()
    # File location for smmdb-course-viewer, get the index
    driver.get(f"file://{os.getcwd()}/smm-course-viewer/index.html")
    # Will upload the cdt file, needs to be in the same working directory as main.

    driver.find_element_by_id("inputFile").send_keys(course_data_loc)
    # Retrieves all the objects
    objects = driver.execute_script("return smmCourseViewer")["objects"]

    driver.close()

    return objects
