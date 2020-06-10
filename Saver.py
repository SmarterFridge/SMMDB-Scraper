import os
import json
from enum import Enum

use_sql = True
try:
    import DBConnection
except ImportError as e:
    print('Avoiding using MySQL, failed to load dependency')
    print(e)
    use_sql = False

class StorageMethod(Enum):
    SQL = 0
    JSON = 1

class Saver:
    """
    Interface for Saver objects
    """
    def save_course(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

class SQLSaver(Saver):
    def __init__(self):
        self.db_connection = DBConnection.DBConnectionInit()
        self.db_cursor = db_connection.cursor()
        self.DBConnection.DBTableCreation(db_cursor)

        assert use_sql, 'Need to have `mysql` installed and functioning before SQLSaver can be used'

    def save_course_metadata(self, course):
        if "description" in course:
            if len(course["description"]) > 100:
                course["description"] = course["description"][:99]

        elif "description" not in course:
            course["description"] = None

        self.db_cursor.execute("INSERT INTO courses (id , "
                          "title, maker, gameStyle, courseTheme, "
                          "courseThemeSub, time, autoScroll, autoScrollSub, width, widthSub, "
                          "owner, nintendoid, videoid, difficulty, "
                          "lastmodified, uploaded, stars, "
                          "description, uploader) "
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                          "%s, %s, %s, %s, %s, %s)",
                          (course["id"],
                           course["title"], course["maker"], course["gameStyle"],
                           course["courseTheme"], course["courseThemeSub"], course["time"], course["autoScroll"],
                           course["autoScrollSub"], course["width"], course["widthSub"], course["owner"],
                           course["nintendoid"],
                           course["videoid"], course["difficulty"], course["lastmodified"], course["uploaded"],
                           course["stars"], course["description"],
                           course["uploader"]))

    def save_course_object(self, course_id, obj):
        self.db_cursor.execute("INSERT INTO objects (courseName, childFlags, childTransform, childType, direction, effect, "
                          "extend, extendedData, flags, height, linkId, id, size, subType, transform, type, "
                          "width, wing, x, y, z) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                          "%s, %s, %s, %s, %s, %s, %s)",
                          (course_id,
                           object["childFlags"], object["childTransform"], object["childType"], object["direction"],
                           object["effect"], object["extend"], object["extendedData"], object["flags"],
                           object["height"], object["linkId"], object["id"], object["size"], object["subType"],
                           object["transform"], object["type"], object["width"], object["wing"], object["x"],
                           object["y"], object["z"]))

    def save_course_objects(self, course_id, objects):
        for obj in objects:
            # Set None objs if the obj does not have them
            if "direction" not in obj:
                obj["direction"] = None

            if "subType" not in obj:
                obj["subType"] = None

            if "wing" not in obj:
                obj["wing"] = None

            if "extend" not in obj:
                obj["extend"] = None

            for key in obj.keys():
                if isinstance(obj[key], list):
                    # Do we want to preserve this data?
                    if len(obj[key]) == 0:
                        obj[key] = None
                    else:
                        obj[key] = ' '.join(map(str, obj[key]))

            self.save_course_object(course_id, obj)

    def save_course(self, course, objects):
        self.save_course_metadata(course)
        self.save_course_objects(self, course['id'], objects)

    def save(self):
        self.db_connection.commit()


class JSONSaver(Saver):
    def __init__(self):
        self.courses = {}

    def __contains__(self, course_id):
        return f'{course_id}.json' in os.listdir('course_data')

    def save_course_metadata(self, course):
        self.courses[course['id']] = {}
        for key, val in filter(lambda x: x[0] != 'id', course.items()):
            self.courses[course['id']][key] = val

    def save_course_objects(self, course_id, objects):
        self.courses[course_id]['objects'] = objects

    def save(self):
        for key in list(self.courses.keys()):
            json.dump(self.courses[key], open(os.path.join('course_data', f'{key}.json'), 'w'))
            del self.courses[key]
