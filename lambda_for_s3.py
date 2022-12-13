import json
import boto3
import csv

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    # TODO implement

    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    csv_file_obj = s3_client.get_object(Bucket=bucket, Key=csv_file)
    lines = csv_file_obj['Body'].read().decode('utf-8').split()
    results = []
    for row in csv.DictReader(lines):
        results.append(row.values())
    print(results)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
