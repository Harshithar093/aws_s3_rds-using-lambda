import csv

#fileds
fields = ['empid','empname','empaddress']

#data for rows of csv file
rows= [['100','Nikhil','Hyd'],['200','shreya','Bng']]


#creating a  csv file
with open('employee.csv', 'w',newline='') as csvfile:
    #creating the csv write object
    empwriter=csv.writer(csvfile)
    #writing the fields
    empwriter.writerow(fields)
    #writing the rows
    empwriter.writerows(rows)

