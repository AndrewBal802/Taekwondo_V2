# import the necessary packages
import cv2
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import csv
from datetime import datetime, timedelta
import os.path
import time
from app import accessDBFiles
import sqlite3
from sqlite3 import Error

DATABASE = 'Data/info.db'


class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = VideoStream(src=0).start() 
       self.currentQRCodes = ""
       self.currentDateForFile = None
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def readCSVFile(self):
        try:
            data = []
            with open("Data/LoginTimes/"+self.currentDateForFile+".csv",'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    data.append(row)
                return data
        except FileNotFoundError:
            return None

    def findCurrentNameInCSV(self,data,name):
        name_id_col = 1
        for i in range(len(data)):
            if (data[i][name_id_col] == name):
                return True #name exists in data
        return False #name doesn't exist in data
    
    def getQRCodes(self):
        return self.currentQRCodes

    def checkValidLoginTime(self):
        currentMin = int(datetime.now().strftime('%M'))
        currentHour = int(datetime.now().strftime('%H'))
        
        #students can only login 15 min prior and 15 mins after the hour
        if (15 < currentMin and currentMin < 45): 
            return False


    def get_frame(self):
        frame = self.video.read()
        frame = imutils.resize(frame, width=700)
        cv2.putText(frame,self.currentQRCodes, (25,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)

    
       
        currentMin = int(datetime.now().strftime('%M'))
        currentHour = int(datetime.now().strftime('%H'))
        if (45 < currentMin and currentMin < 60):
            currentTime = datetime.now()
            addedTime = timedelta(hours=1)
            currentTime += addedTime
            self.currentDateForFile = currentTime
            self.currentDateForFile = self.currentDateForFile.strftime('%Y-%m-%d-%H')
        elif(0 <= currentMin and currentMin <= 15):
            self.currentDateForFile = datetime.now().strftime('%Y-%m-%d-%H')
        
        else:
            cv2.putText(frame,"You can only sign in between " + str(currentHour)+":45 and " + str((currentHour+1))+":15" , (25,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes() 
       

        #getting current data from CSV file
        data = []
        if self.readCSVFile() != None:
            data = self.readCSVFile()
        
         #determine whether to write(create new file) or append to new file
        mode = ''
        if (os.path.exists("Data/LoginTimes/"+self.currentDateForFile+".csv") == True):
            mode = 'a'
        else:
            mode = 'w'
        
        currentStudent = ""
        #open csv file and write data to it and determine the QR code using opencv


        with open("Data/LoginTimes/"+self.currentDateForFile+".csv",mode,newline='') as file:
            writer = csv.writer(file)
            # loop over the detected barcodes
            for barcode in barcodes:
                    # extract the bounding box location of the barcode and draw
                    # the bounding box surrounding the barcode on the image
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # the barcode data is a bytes object so if we want to draw it
                    # on our output image we need to convert it to a string first
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    
                    
                    self.currentQRCodes = barcodeData

                    # draw the barcode data and barcode type on the image
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    #data = self.readCSVFile()

                    
                    currentStudent = ""
                    statusOfLoggedInStudent = False
                    currentHour = datetime.now().strftime('%H %p')
                    if (self.findCurrentNameInCSV(data,barcodeData) == False):
                        print(barcodeData)
                        writer.writerow([datetime.now().strftime('%Y-%m-%d %I:%M'),barcodeData])
                        self.currentQRCodes = barcodeData + " you have signed in for " + currentHour + " class !"
                        

                        ID = barcodeData.split("_")[2]
                        conn = create_connection()
                        accessDBFiles.appendLoginInfo(conn,datetime.now().strftime('%Y-%m-%d %I:%M'), ID)
                        
                    else:
                        #self.currentQRCodes = barcodeData + " you are already signed in!"
                        self.currentQRCodes = barcodeData + " you have signed in for " + currentHour + " class !"
                    #cv2.putText(frame,currentStudent, (25,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            
            # show the output frame
            #cv2.imshow("Barcode Scanner", frame)
            #cv2.putText(frame,currentQRCodes, (25,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2) 
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except Error as e:
        print(e)

    return conn


