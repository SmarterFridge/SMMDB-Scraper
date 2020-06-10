import os

import ObjectGrabber
import Downloader
from Saver import Saver, JSONSaver

def main(saver: Saver):
    assert isinstance(saver, Saver)

    for course in filter(lambda course: course['id'] not in saver, Downloader.get_all_info()):
        if "description" in course:
            if len(course["description"]) > 100:
                course["description"] = course["description"][:99]

        elif "description" not in course:
            course["description"] = None

        saver.save_course_metadata(course)
        course_id = course["id"]
        print('Downloading', course['title'])
        if not len(course['title'].strip()):
            continue

        Downloader.download_via_id(course_id)

        # Get the objects and course name from the selenium web page
        course_path = os.path.join(os.getcwd(), 'courses', course_id, 'course000')

        try:
            filenames = os.listdir(course_path)
        except FileNotFoundError:
            continue

        for filename in filter(lambda x: 'cdt' in x, filenames):
            objects = ObjectGrabber.ObjectGrabber(os.path.join(course_path, filename))

            if objects is None:
                continue

            for object in objects:

                object['which_course'] = filename.split('.')[0]

                # Set None objects if the object does not have them
                if "direction" not in object:
                    object["direction"] = None

                if "subType" not in object:
                    object["subType"] = None

                if "wing" not in object:
                    object["wing"] = None

                if "extend" not in object:
                    object["extend"] = None

                for key in object.keys():
                    if isinstance(object[key], list):
                        # Do we want to preserve this data?
                        if len(object[key]) == 0:
                            object[key] = None
                        else:
                            object[key] = ' '.join(map(str, object[key]))

            saver.save_course_objects(course_id, objects)
        print('saving...')
        saver.save()


if __name__ == "__main__":
    saver = JSONSaver()
    main(saver)
