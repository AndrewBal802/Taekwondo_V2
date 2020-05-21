from app import app
from flask import Flask, flash, redirect, render_template, request, url_for, g, Response
import os
import sqlite3
from sqlite3 import Error
from app import accessDBFiles
from app import createXLS
#from app import Camera
from app import openCVQRCODE
import time
DATABASE = 'Data/info.db'
app.secret_key = 'random string'

@app.route('/', methods = ['GET', 'POST'])
def home():
    error = None
    print(readCred())
    cred = readCred()
    if (request.method == 'POST'):
        if  (request.form['username'] == cred[0]  and request.form['password'] == cred[1]):
            return redirect(url_for('instructor'))
        else:
            flash("Incorrect Creditionals")
            error = 'Invalid userName or password. Please try again!.'
            print("WRONG CREDs")
    return render_template('home.html', error = error)


@app.route('/instructor', methods = ['GET', 'POST'])
def instructor():

    return render_template('instructor.html')


@app.route('/instructor/findStudent',  methods = ['GET', 'POST'])
def findStudent():
    error = None
    if (request.method == 'POST'):
        #getting first and last name from textbox
        firstName = request.form['firstName']
        lastName = request.form['lastName']

        firstName = firstName[0].upper() + firstName[1:].lower()
        lastName = lastName[0].upper() + lastName[1:].lower()
        #finding current indivudal
        conn = create_connection()

        info = accessDBFiles.findStudent(conn,firstName,lastName)

        if (info == None):
            error = firstName + " " + lastName + " does not exist in current student Data Base!"
        else:
            return redirect(url_for('viewStudent',fullName = firstName+"_"+lastName))

    return render_template('findStudent.html',error = error)


@app.route('/instructor/findStudent/viewStudent/<fullName>', methods = ['GET', 'POST'])
def viewStudent(fullName):
    status = None
    success = False
    splitFullName = fullName.split("_")
    firstName = splitFullName[0]
    lastName = splitFullName[1]

    conn = create_connection()
    info = accessDBFiles.findStudent(conn,firstName,lastName)

    loginInfo = info[-1]

    colHeading = accessDBFiles.getColumnNames(conn)
   #begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,
   #BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS)
    if (request.method == 'POST'):
        with conn:
            begin_date = request.form['begin_date']
            WHITE_Belt = request.form['WHITE_Belt']
            YELLOW_Stripe_Belt = request.form['YELLOW_Stripe_Belt']
            YELLOW_Belt = request.form['YELLOW_Belt']
            GREEN_Stripe_Belt = request.form['GREEN_Stripe_Belt']
            GREEN_Belt = request.form['GREEN_Belt']
            BLUE_Stripe_Belt = request.form['BLUE_Stripe_Belt']
            BLUE_Belt = request.form['BLUE_Belt']
            RED_Stripe_Belt = request.form['RED_Stripe_Belt']
            RED_Belt = request.form['RED_Belt']
            BLACK_Stripe_Belt = request.form['BLACK_Stripe_Belt']
            BLACK_Belt = request.form['BLACK_Belt']
            COMMENTS = request.form['COMMENTS']
            ID = info[0]

            print(COMMENTS, ID)
            print(info[-1])
            success = accessDBFiles.updateBeltInfo(conn,ID,begin_date,WHITE_Belt,YELLOW_Stripe_Belt,
                    YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,
                    RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS)
            if (success == True):
                status = "You have successively updated " + firstName + " " + lastName + "'s information"
                info = (info[0],info[1],info[2], begin_date,WHITE_Belt,YELLOW_Stripe_Belt,
                        YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,
                        RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS)

                #return redirect(url_for('viewStudent',fullName = fullName),status)


    return render_template('viewStudent.html', firstName = firstName, \
            lastName = lastName,colHeading = colHeading, info = info, success = success, status = status, loginInfo = loginInfo)


@app.route('/instructor/addStudent', methods = ['GET', 'POST'])
def addStudent():
    success = None
    if (request.method == 'POST'):
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        startDate = request.form['startDate']

        conn = create_connection()
        currentStatus = accessDBFiles.addStudent(conn,firstName,lastName,startDate)
        if currentStatus == True:
            success = "Added " + firstName + " " + lastName + " has been added successively!"
    return render_template('addStudent.html',success = success )


#assuming that the dates in date base have been entered as yyyy-mm-dd
#TODO: - add a check for adding/adjusting the month of a student following the same format as "yyyy-mm-dd"
@app.route('/instructor/testingMonth', methods = ['GET', 'POST'])
def testingMonth():
    status = None
    date = None
    if (request.method == 'POST'):
        date = request.form['date']

        conn = create_connection()
        listOfStudents = accessDBFiles.findStudentsAtSpecifcDate(conn,date)
        if (len(listOfStudents) != 0):
            status = "A testingMonth.xls file has been produced with a list of students testing in "

            xlsFileLoc = "Data/testingMonth.xls"
            createXLS.writeToFile(xlsFileLoc,listOfStudents,date)
        else:
            status = "There are no students schedule to test in "
        print(listOfStudents)
    return render_template('testingMonth.html',status = status, date = date)

def readCred():
    f = open("Data/Credentials.txt","r")
    arrayList = []

    arrayList.append(f.readline().strip('\n')) #username
    arrayList.append(f.readline().strip('\n')) #password

    f.close()
    return arrayList

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    """conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

currentStudentLogin = ""
videoCamera = None
@app.route('/qrCode')
def qrCode():
    currentStudent = None
    if (videoCamera != None):
        currentStudent = videoCamera.getQRCodes()

    return render_template('quickLoginQRCODE.html',currentStudent = currentStudent)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    videoCamera = openCVQRCODE.VideoCamera()
    return Response(gen(videoCamera), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(debug=True,use_reloader=True)
