import xlrd 
import xlwt
from xlutils.copy import copy

def loadXLSFile(loc):
    wb = xlrd.open_workbook(loc,formatting_info=True) 
    sheet = wb.sheet_by_index(0)
    writeBack = copy(wb)

    return writeBack

def writeToFile(location,data, date):


    writeBack = loadXLSFile(location)
    w_sheet = writeBack.get_sheet(0)

    style = xlwt.easyxf('font: bold 1,height 280;')
    w_sheet.write(0,0,"Testing for the current date of " + date, style)
    
    currentRow = 2 #starting at the third row
    currentCol = 0
    for i in range(len(data)):
        for j in range (len(data[i])):
            w_sheet.write(currentRow,currentCol,data[i][j])
            currentCol += 1

        currentCol = 0
        currentRow += 1 

    writeBack.save(location)

