from app import app
from flask import Flask, flash, redirect, render_template, request, url_for, g 
import os
import sqlite3
from sqlite3 import Error 
from app import accessDBFiles

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
            error = firstName + " " + lastName + " Does not exist in current Data Base (info.db)"
        else:
            return redirect(url_for('viewStudent',fullName = firstName+"_"+lastName))
    else:
        print()

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
    
    colHeading = accessDBFiles.getColumnNames(conn)
   #begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS)
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
            success = accessDBFiles.updateBeltInfo(conn,ID,begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS)
            if (success == True):
                status = "You have successively updated " + firstName + " " + lastName + "'s information"
                info = (info[0],info[1],info[2], begin_date,WHITE_Belt,YELLOW_Stripe_Belt,YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS) 

                #return redirect(url_for('viewStudent',fullName = fullName),status) 


    return render_template('viewStudent.html', firstName = firstName, \
            lastName = lastName,colHeading = colHeading, info = info, success = success, status = status)


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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
       app.run(debug = True)

