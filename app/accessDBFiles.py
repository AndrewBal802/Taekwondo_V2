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
                                        Login_Times text
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

    sql = ''' INSERT INTO students(firstName,lastName,begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS,Login_Times)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
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
        info = (firstName,lastName,startDate,'','','','','','','','','','','','','')
        insertData(conn,info)

    return True

#TODO: update getColumnNames function name to getStudentHeader(conn)
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

def updateBeltInfo(conn,ID,begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,
        BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS):
   
    with conn:
        info = (begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,
                BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS,ID)
        print(info)
        print(type(info))
        updatingInfo(conn,info)
        
        return True

    return False

def findStudentsAtSpecifcDate(conn,date):
    cursor = conn.cursor()
    select_query = """ SELECT * from students"""
    cursor.execute(select_query)
    records = cursor.fetchall() #2D array

    
    collectedStudents = []
    colHeadingNames = getColumnNames(conn)
    
    colTracker = 0
    for row in records:
        for info in row:
            if (info == date and colTracker > 3):
                currentStudentInfo = [row[0],row[1],row[2],colHeadingNames[colTracker]]
                collectedStudents.append(currentStudentInfo) #appending the students ID number, first and last name
                break
            colTracker += 1
        colTracker = 0

    cursor.close()
    return collectedStudents


def getLoginInfo(conn,ID):
    cursor = conn.cursor()
    select_query = ''' SELECT Login_Times from students WHERE id = ?'''
    info = (ID,)
    cursor.execute(select_query, info)
    records = cursor.fetchall() #2D array

    currentLoginInfo = ""
    for data in records: #list
        for info in data: #tuple
            currentLoginInfo = info
    return currentLoginInfo



def appendLoginInfo(conn,loginTime,ID):
    getCurrentLogin = getLoginInfo(conn,ID)
    sql = ''' UPDATE students
              SET Login_Times = ?
              WHERE id = ? '''
    if (getCurrentLogin == None):
        getCurrentLogin = loginTime + "\n"
    else:
        getCurrentLogin = getCurrentLogin +  "\n" + loginTime + "\n"
    with conn:
        cur = conn.cursor()
        info = (getCurrentLogin,ID)
        cur.execute(sql, info)
        conn.commit()

def getInventoryHeader(conn):
    cursor = conn.cursor()
    #select_query = """ SELECT * from inventory"""
    select_query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(select_query)
    
    colNames = cursor.fetchall() #returns a list of single tuples with the names of all tables in the database

    colNames.remove(('students',)) #removing student table from inventory

    names = []
    for namesList in colNames:
        for namesTuple in namesList:
            names.append(namesTuple)

    return names

def checkForIfInventoryHeaderExists(conn,currentName):
    arrayNames = getInventoryHeader(conn)
    
    if (currentName in arrayNames):
        return True #name exists
    else:
        return False #name doesnt exists
    

def insertInventoryCategory(conn,colName):
    if (len(colName) == 0 or checkForIfInventoryHeaderExists(conn,colName) == True):
        return

    cursor = conn.cursor() 
    info = (colName,)
    #cursor.execute('''ALTER TABLE inventory ADD COLUMN ? text''', info) #this currrent method doesnt work

    #need to double check if this method is select_query
    #cursor.execute("ALTER TABLE inventory ADD COLUMN '{name}' text".format(name=colName))
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS '{tableName}'(id integer PRIMARY KEY, '{colName}' text NOT NULL)'''
            .format(tableName=colName,colName=colName))
    return

def getInventoryCategoryData(conn,tableName):
    cursor = conn.cursor()
    #if you replace * with '{tableName}' there is a strange bug
    cursor.execute('''SELECT * FROM '{tableName}' '''.format(tableName=tableName)) 

    rows = cursor.fetchall()
    #print(rows)
    data = []

    for item in rows:
        data.append(item[1].strip()) #item will be a tuple of (id, colData)
    return data

#need to find a more efficient method, because there several empty spaces
def addInventoryItems(conn,colName,item):
    if (len(item) == 0):
        return False
    cursor = conn.cursor()
    cursor.execute("INSERT INTO '{tableName}'( '{colName}' ) VALUES ( '{item}' )"
        .format(tableName=colName,colName=colName,item=item))
    conn.commit()
    return True 

def updateInventoryItems(conn,colName,itemList):
    if (len(itemList) == 0):
        return False

    cursor = conn.cursor()
    for i in range(len(itemList)):
        info = (itemList[i][1], itemList[i][0])
        cursor.execute(" UPDATE '{tableName}' SET '{colName}' = ? where id = ? ".format(tableName=colName,colName=colName),info)
        conn.commit()
    return True

"""NOTES:
    to add column in .db file, "ALTER TABLE table_name ADD Login_Times NULL";
"""

#print(findStudent("Andrew","Balmakund"))
#addStudent("Brian","Balmakund","2020-05-05")
#print(findStudent("BRIAN","BALMAKUND"))
#if __name__ == '__main__':
#    main()
