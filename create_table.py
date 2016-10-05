from __future__ import print_function # Python 2/3 compatibility
import boto3
import tconf

#url="https://dynamodb.eu-central-1.amazonaws.com"
#region="eu-central-1"

dynamodb = boto3.resource('dynamodb', region_name=tconf.region, endpoint_url=tconf.url)


table = dynamodb.create_table(
    TableName = 'Temperature',
    KeySchema = [       
        { 'AttributeName': 'Thermometer', 'KeyType': 'HASH' }, # //Partition key
        { 'AttributeName': 'GetDate', 'KeyType': 'RANGE' }  #//Sort key
    ],
    AttributeDefinitions = [       
        { 'AttributeName': 'Thermometer', 'AttributeType': 'S' },
        { 'AttributeName': 'GetDate', 'AttributeType': 'N' },
    ],
    ProvisionedThroughput = {       
        'ReadCapacityUnits': 10, 
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
