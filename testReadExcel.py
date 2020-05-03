import xlrd 
import xlwt
from xlutils.copy import copy
loc = ("STUDENT BELT PROGRESS.xls") 
  
wb = xlrd.open_workbook(loc,formatting_info=True) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
  
for i in range(sheet.nrows): 
    print(sheet.cell_value(i, 0))

print(sheet.row_values(5))


#note format changes
writeBack = copy(wb)
w_sheet = writeBack.get_sheet(0)
w_sheet.write(sheet.nrows,0,"Andrew Balmakund")
writeBack.save(loc)

