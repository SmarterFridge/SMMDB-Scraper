import mysql.connector


# Will return a cursor and DB object in a list as [cursor, DB]
def DBConnectionInit():
    # Connect to the DB and credentials
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456"
    )

    # Database details
    db_name = "MarioMakerDB"
    db_cursor = db_connection.cursor()
    db_cursor.execute("SHOW DATABASES")

    # Set the connection if database has not been made
    if (db_name.lower(),) not in db_cursor:
        db_cursor.execute("CREATE DATABASE {}".format(db_name))

    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database=db_name
    )

    return db_connection


# Creates the Tables, if not already present
def DBTableCreation(db_cursor):

    table = "objects"
    stmt = "SHOW TABLES LIKE '{}'".format(table)
    db_cursor.execute(stmt)
    result_obj = db_cursor.fetchone()
    # Create the table
    if not result_obj:
        db_cursor.execute("CREATE TABLE {} (courseName VARCHAR(255), "
                          "childFlags INT, childTransform INT, childType INT, direction INT, "
                          "effect INT, extend VARCHAR(255), extendedData INT, flags INT, height INT, linkId INT, "
                          "name VARCHAR(255), size INT, subType INT, transform INT, type INT, width INT, wing INT, "
                          "x INT, y INT, z INT)".format(table))

    table = "courses"
    stmt = "SHOW TABLES LIKE '{}'".format(table)
    db_cursor.execute(stmt)
    result_course = db_cursor.fetchone()
    # Create the table
    if not result_course:
        db_cursor.execute("CREATE TABLE {} (id VARCHAR(255) PRIMARY KEY, "
                          "title VARCHAR(255), maker VARCHAR(255), gameStyle INT, courseTheme INT, "
                          "courseThemeSub INT, time INT, autoScroll INT, autoScrollSub INT, width INT, widthSub INT, "
                          "owner VARCHAR(255), nintendoid VARCHAR(255), videoid VARCHAR(255), difficulty INT, "
                          "lastmodified INT, uploaded INT, description VARCHAR(255), "
                          "uploader VARCHAR(255), stars INT)".format(table))

    return None

