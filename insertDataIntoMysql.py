import csv
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


try:
    connection=mysql.connector.connect(host='harshita-instance.czk4p5jjouim.ap-south-1.rds.amazonaws.com',database='employeedb',user='admin',password='adminpassword')
    mysql_empsql_insert_query="INSERT INTO employee (empid,empname,empaddress) values(%s,%s,%s)"
    #mysql_delete_query="DELETE FROM employee WHERE empid IN (100, 200)"
    #rows = [['100', 'Nikhil', 'Hyd'], ['200', 'shreya', 'Bng']]
    rows=[]
    with open('emp_dict.csv',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row.values())

    cursor=connection.cursor()
    cursor.executemany(mysql_empsql_insert_query,rows)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into employee table")

    mysql_select_Query = "select * from employee"
    cursor=connection.cursor()
    cursor.execute(mysql_select_Query)
    records=cursor.fetchall()

    print("Total number of rows in employess table is: ", cursor.rowcount)

    print("\n Printing each employee record")
    for row in records:
        print("empid = ",row[0])
        print("empname = ", row[1])
        print("empaddress = ",row[2])
    cursor.close()

#if it fails to  insert record into table carch in  except class
except mysql.connector.Error as error:
    print("failed to insert record into employee table {}".format((error)))

finally:
    if (connection.is_connected()):
        connection.close()
        print("MySql connection is closed")




