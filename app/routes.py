from app import app
from flask import Flask, flash, redirect, render_template, request, url_for, g, Response
import os
import sqlite3
from sqlite3 import Error
from app import accessDBFiles
from app import createXLS
#from app import Camera
from app import openCVQRCODE
from app import openCVBARCODE
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

    return render_template('instructor.html',instructorActive="active")


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

    return render_template('findStudent.html',findStudentActive="active",error = error)


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
    
    loginInfoList = loginInfo.split("\n")
    loginInfoList.reverse() #latest dates are shown first
    
    loginInfoList = [login for login in loginInfoList if login]

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

                #remove if neccessary
                info = (info[0],info[1],info[2], begin_date,WHITE_Belt,YELLOW_Stripe_Belt,
                        YELLOW_Belt,GREEN_Stripe_Belt,GREEN_Belt,BLUE_Stripe_Belt,BLUE_Belt,RED_Stripe_Belt,
                        RED_Belt,BLACK_Stripe_Belt,BLACK_Belt,COMMENTS)

                #return redirect(url_for('viewStudent',fullName = fullName),status)
    return render_template('viewStudent.html', findStudentActive="active",firstName = firstName, \
            lastName = lastName,colHeading = colHeading, info = info, success = success, status = status, 
            loginInfo = loginInfoList )
 
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
    return render_template('addStudent.html',addStudentActive="active",success = success )



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
    return render_template('testingMonth.html',testingMonthActive="active",status = status, date = date)


def readCred():
    f = open("Data/Credentials.txt","r")
    arrayList = []

    arrayList.append(f.readline().strip('\n')) #username
    arrayList.append(f.readline().strip('\n')) #password

    f.close()
    return arrayList


currentStudentLogin = ""
videoCamera = None
@app.route('/qrCode')
def qrCode():
    currentStudent = None
    if (videoCamera != None):
        currentStudent = videoCamera.getQRCodes()

    return render_template('quickLoginQRCODE.html',qrCodeActive="active",currentStudent = currentStudent)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed_QR')
def video_feed_QR():
    videoCamera = openCVQRCODE.VideoCamera()
    return Response(gen(videoCamera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/inventory', methods = ['GET','POST'])
def inventory():
    conn = create_connection()
    colHeading = accessDBFiles.getInventoryHeader(conn)
    colHeading.sort()
    info = None
    currentUserSelection = None

    if (request.method == 'POST'):
        currentUserSelection = str(request.form['colHeading'])
        if (request.form['submitButton'] == 'Get Info'):
            print(str(request.form['colHeading']))
            info = accessDBFiles.getInventoryCategoryData(conn,currentUserSelection)
            #currentUserSelection = str(request.form['colHeading'])

        elif (request.form['submitButton'] == 'Create New Heading'):
            print(str(request.form['headerName']))
            newHeaderName = str(request.form['headerName'])
            accessDBFiles.insertInventoryCategory(conn,newHeaderName)
            return redirect(url_for('inventory'))

        elif (request.form['submitButton'] == "Enter Items"):
            #headerName = str(request.form['colHeading'])
            headerName = currentUserSelection
            itemName = str(request.form['itemText']).strip()
            quantity = str(request.form['newQuantity']).strip()

            itemStr = itemName + "-"+ quantity
            #print(headerName,itemStr, "NEW ITEM ADDED")
            accessDBFiles.addInventoryItems(conn,headerName,itemStr)

            print(headerName,itemStr, "NEW ITEM ADDED")


        elif (request.form['submitButton'] == "Save"):
            currentItems = accessDBFiles.getInventoryCategoryData(conn,currentUserSelection)
            numOfItems = len(currentItems)

            updatedItems = [] #list of tuple's: (id, colData)
            for i in range(numOfItems):
                currentRow = i+1

                itemName = str(request.form["itemName-%s" % currentRow]).strip()
                quantity = str(request.form["quantity-%s" % currentRow]).strip()

                concatInfo = itemName + "-" + quantity
                print(concatInfo)

                #updatedItems.append((currentRow,request.form['%s' % currentRow]))
                updatedItems.append((currentRow, concatInfo.strip()))

            print(updatedItems)
            accessDBFiles.updateInventoryItems(conn,currentUserSelection,updatedItems)

    return render_template('viewInventory.html', inventoryActive="active",colHeading = colHeading, info = info ,
            currentUserSelection = currentUserSelection)


@app.route('/quick_inventory', methods = ['GET','POST']) 
def quick_inventory():
    if (request.method == 'POST'):
        if (request.form['submitButton'] == "Check Out"):
            return redirect(url_for('quick_inventory_checkout'))
        elif (request.form['submitButton'] == "Return"):
            return redirect(url_for('quick_inventory_return'))

    return render_template('quickInventory.html',quickInventoryActive="active")



@app.route('/quick_inventory_checkout', methods = ['GET','POST'])
def quick_inventory_checkout():
    return render_template('quickInventoryCheckout.html')



@app.route('/video_feed_barcode_checkout')
def video_feed_BARCODE_checkout():
    videoCamera = openCVBARCODE.BarCodeReader() #instantiating barcode object
    return Response(gen(videoCamera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/quick_inventory_return', methods = ['GET','POST'])
def quick_inventory_return():
    return render_template('quickInventoryCheckout.html')


"""
@app.route('/video_feed_barcode_return')
def video_feed_BARCODE_return():
    videoCamera = openCVBARCODE.BarCodeReader() #instantiating barcode object
    return Response(gen(videoCamera), mimetype='multipart/x-mixed-replace; boundary=frame')
"""


def create_connection():
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
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(debug=True,use_reloader=True)
