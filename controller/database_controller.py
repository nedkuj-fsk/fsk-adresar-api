import sqlite3

database_name = 'students.db'

isInitialised = False


def init():
    global connection
    connection = sqlite3.connect(database_name)
    connection.row_factory = dict_factory
    global cursor
    cursor = connection.cursor()
    isInitialised = True


def dict_factory(c, row):
    d = {}
    for idx, col in enumerate(c.description):
        d[col[0]] = row[idx]
    return d


def createDatabase():
    if not isInitialised:
        init()

    # Create the table
    cursor.execute('CREATE TABLE students ('
                   'studentId VARCHAR PRIMARY KEY NOT NULL, '
                   'firstName VARCHAR NOT NULL, '
                   'lastName VARCHAR NOT NULL,'
                   'department VARCHAR NOT NULL,'
                   'cycle INTEGER NOT NULL,'
                   'semester INTEGER NOT NULL'
                   ')')


def insert_student(student):
    if not isInitialised:
        init()

    cursor.execute(f'INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)',
                   (student.studentId,
                    student.firstName,
                    student.lastName,
                    student.department,
                    student.cycle,
                    student.semester)
                   )
    connection.commit()


def get_students():
    if not isInitialised:
        init()

    cursor.execute('SELECT * FROM students')
    data = cursor.fetchall()
    return data


def get_student(student_id):
    if not isInitialised:
        init()

    cursor.execute(f'SELECT * FROM students WHERE studentId = "{student_id}"')
    data = cursor.fetchone()
    return data


def empty_database():
    if not isInitialised:
        init()
    cursor.execute('DROP TABLE students')
    connection.commit()
