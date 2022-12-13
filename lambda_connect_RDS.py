import json
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


def lambda_handler(event, context):
    # TODO implement
    connection = mysql.connector.connect(host='harshita-instance.czk4p5jjouim.ap-south-1.rds.amazonaws.com',
                                         database='employeedb', user='admin', password='adminpassword')
    mysql_empsql_insert_query = "INSERT INTO employee (empid,empname,empaddress) values(%s,%s,%s)"
    rows = [['500', 'tejesh', 'KARNATAKA'], ['600', 'laxmi', 'BELGAM']]
    cursor = connection.cursor()
    cursor.executemany(mysql_empsql_insert_query, rows)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into employee table")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
