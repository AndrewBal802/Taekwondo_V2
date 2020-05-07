import sqlite3
from sqlite3 import Error
from app import routes

"""
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
"""

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def MainFun():
    database = r"../Data/info.db"

    sql_create_student_table = """ CREATE TABLE IF NOT EXISTS students (
                                        id integer PRIMARY KEY,
                                        firstName text NOT NULL,
					lastName text NOT NULL,
                                        begin_date text,
                                        WHITE_Belt text,
                                        YELLOW_Stripe_Belt text,
                                        YELLOW_Belt text,
                                        GREEN_Stripe_Belt text,
                                        GREEN_Belt text,
                                        BLUE_Stripe_Belt text,
                                        BLUE_Belt text,
                                        RED_Stripe_Belt text,
                                        RED_Belt text,
                                        BLACK_Stripe_Belt text,
                                        BLACK_Belt text,
					COMMENTS text
                                    ); """


    # create a database connection
    conn = routes.create_connection(database)

    
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_student_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        info = ('ANDREW','BALMAKUND','2014-01-01','2014-01-01','2014-02-01','2014-03-03','2014-04-01','2014-05-01','2014-06-01','2014-07-01','2014-08-01','2014-09-01','2014-10-01','2014-11-01', 'None')
        insertData(conn,info)

    #print(findStudent(conn,"Andrew","Balmakund"))

def insertData(conn,info):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO students(firstName,lastName,begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, info)
    return cur.lastrowid

def connectDataBase():
    database = r"../Data/info.db"
    conn = routes.create_connection(database)
    return conn 


def addStudent(conn,firstName,lastName,startDate):
    if (findStudent(conn,firstName,lastName) != None): #if student already exist in database
        return False #no student has been added
    with conn:
        info = (firstName,lastName,startDate,'','','','','','','','','','','','')
        insertData(conn,info)

    return True

def getColumnNames(conn):
    cursor = conn.cursor()
    select_query = """ SELECT * from students"""
    cursor.execute(select_query)
    colNames = [tuple[0] for tuple in cursor.description]
    
    return colNames



def findStudent(conn,firstName,lastName):
    cursor = conn.cursor()
    select_query = """ SELECT * from students"""
    cursor.execute(select_query)
    records = cursor.fetchall() #2D array

    for row in records:
        if (row[1].lower() == firstName.lower() and row[2].lower() == lastName.lower()):
            return row
    cursor.close()
    return None

def updatingInfo(conn,info):
    sql = ''' UPDATE students
              SET begin_date = ?,
                        WHITE_Belt = ?,
                        YELLOW_Stripe_Belt = ?,
                        YELLOW_Belt = ?,
                        GREEN_Stripe_Belt = ?,
                        GREEN_Belt = ?,
                        BLUE_Stripe_Belt = ?,
                        BLUE_Belt = ?,
                        RED_Stripe_Belt = ?,
                        RED_Belt = ?,
                        BLACK_Stripe_Belt = ?,
                        BLACK_Belt = ?,
                        COMMENTS = ?
              WHERE id = ? '''
    
    cur = conn.cursor()
    cur.execute(sql, info)
    conn.commit()

def updateBeltInfo(conn,ID,begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS):
   
    with conn:
        info = (begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS,ID)
        updatingInfo(conn,info)
        
        return True

    return False

#print(findStudent("Andrew","Balmakund"))
#addStudent("Brian","Balmakund","2020-05-05")
#print(findStudent("BRIAN","BALMAKUND"))
#if __name__ == '__main__':
#    main()
