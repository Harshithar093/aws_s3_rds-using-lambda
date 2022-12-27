# aws_s3_rds-using-lambda
Load the csv from  amazon s3 to RDS database using lambda function
![image](https://user-images.githubusercontent.com/110849641/207369735-ae3a997c-3fa6-479e-ad96-df5f4d3f4d99.png)
Amazon s3 service:
Used for file storage,where you can upload or remove files.We can trigger AWS Lambda on S3 when there are any file uploads in S3 buckets.AWS Lambda has a handler function which acts as a point for AWS Lambda function.The handler has the details of teh events.
Steps for Using AWS Lambda Function with Amazon S3
1.Create S3 Bucket->bucketname
2.Create role.this role is for Allow lambda functn have permission to access S3,cloudwatch,RDS.(services->IAM->Roles->create role->select AWS service(ec2,Lambda and others)->next permissions->Filter policies-> choose 1.AmazonS3FullAccess 2.cloudwatchfullaccess 3.AmazonRDSFullAccess-> next tag-> review-> create role->rolename:lambda-role-for-app1-for-s3-cloudwatch-rds->enter create role
3.Create Lambda function and add S3 as the trigger.(Lambda->Functions->create function-> basic Info(Function name:ReadDataFrom AmazonS3, Runtime python 3.8, permissions ->choose or create an execution role(Existing-role) ->choose step2 created role(lambda-role-for-app1-for-s3-cloudwatch-rds)-> create function.
4.Add trigger: Go to Lambda>Functions>ReadDataFromAmazonS3 > click on +Add trigger > Trigger configuration ->choose S3-> select Bucket(name from step1)>Event Type-> All object creaet event>prefix="if any folder is created inside that bucket give that folder name" ,suffix>to limit notifications we enter which type of data format i.e ".csv" > Enable trigger > I Acknowldge > ADD
Go to ReadDataFromAmazonS3 Function Code add print(events) inside lambda function ,save,deploy.
5. GO to S3 bucket and uplaod the csv file under that folder.
6. Go to cloudwatch->log groups. A Log group will be created from our Lambda function name(/aws/lambda/ReadDataFromAmazonS3)> click on Latest Logstream > Timesatmp mesage > can see the event printed in Logs- copy that record which contains S3 bucket data -view in online json viewer> u can know s3 bucket name and event name-bucket=events[records][0][s3][bucket[name],csv_file=events['records'][0]['s3']['object']['key'], use s3 client to get object, csv_file_obj=(Bucket=bucekt name and key=csv_file)
ReadDataFromAWSS3 lambda function before adding RDS lambda function:

import json
import boto3
import csv

s3_client=boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    
    bucket=event['Records'][0]['s3']['bucket']['name']
    csv_file =event['Records'][0]['s3']['object']['key']
    csv_file_obj = s3_client.get_object(Bucket=bucket,Key=csv_file)
    lines = csv_file_obj['Body'].read().decode('utf-8').split()
    results=[]
    for row in csv.DictReader(lines):
        results.append(row.values())
    print(results)    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


Once the file is uplaoded it will trigger AWS Lambda function in the background which will dispaly an output in the form of console mesages,user will be able to the messages in the cloudwatch logs once the file is uploaded.

create a Amazon RDS instance and db, check wether its free tier. Also setup a mysql workbench in local .(give inbound and outbound traffic anywhere in connectivity and security  so taht it allows all traffic if u wnt to connect from public) copy the RDS endpoint adress/url from aws and connect in workbench. connect to AWS RDS,create a database,cretae tables.
Mysql Database Connection in Python
![image](https://user-images.githubusercontent.com/110849641/209417402-04f691de-3a0d-45f2-8124-e34aaa535971.png)
just create a insertdataintomysql.py and check wethr u able to connect to RDS and insert the data from csv.

2.Connecting to RDS using Lambda layer
check Roles -> AmazonRDS FullAccess,AmazonS3FullAccess,CloudWatchFullAccess
1.Go to function-> create a function ConnectToRDSUsingPython-> Runtime-> 3.8, choose execution role->choose existing role-> eg:lambda-role-for-app1-for-s3-cwl
2.go to this connectoToRDSUisngPyhon -> write python Lambda function.
Go to readDatafromAWSS3 lambda function and ADD the lambda layer which we added for connecttoRDS lambda.lambda layer has packages dependency i.e mysql connector.
downlaod that dependecy package and add in lambda layer
#connecting to RDS and writing data lambda
import json
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

def lambda_handler(event, context):
    # TODO implement
    connection=mysql.connector.connect(host='harshita-instance.czk4p5jjouim.ap-south-1.rds.amazonaws.com',database='employeedb',user='admin',password='adminpassword')
    mysql_empsql_insert_query="INSERT INTO employee (empid,empname,empaddress) values(%s,%s,%s)"
    rows =[['500','tejesh','KARNATAKA'],['600','laxmi','BELGAM']]
    cursor=connection.cursor()
    cursor.executemany(mysql_empsql_insert_query,rows)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into employee table")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


#Final single Lambda function reading from s3 and writing into AMzon RDS
import json
import boto3
import csv
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

s3_client=boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement

    bucket=event['Records'][0]['s3']['bucket']['name']
    csv_file =event['Records'][0]['s3']['object']['key']
    csv_file_obj = s3_client.get_object(Bucket=bucket,Key=csv_file)
    lines = csv_file_obj['Body'].read().decode('utf-8').split()
    results=[]
    for row in csv.DictReader(lines):
        results.append(row.values())
    print(results) 
    connection=mysql.connector.connect(host='harshita-instance.czk4p5jjouim.ap-south-1.rds.amazonaws.com',database='employeedb',user='admin',password='adminpassword')
    mysql_empsql_insert_query="INSERT INTO employee (empid,empname,empaddress) values(%s,%s,%s)"
    cursor=connection.cursor()
    cursor.executemany(mysql_empsql_insert_query,results)
    connection.commit()
    print(cursor.rowcount, "Record inserted successfully into employee table")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }




