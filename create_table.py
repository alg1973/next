from __future__ import print_function # Python 2/3 compatibility
import boto3
import tconf

#url="https://dynamodb.eu-central-1.amazonaws.com"
#region="eu-central-1"

dynamodb = boto3.resource('dynamodb', region_name=tconf.region, endpoint_url=tconf.url)

print ("Creating 'Temperature' table...")

try:
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
except Exception as e:
	print ("Exception: ", e)


print ("Creating 'Commands' table...")
try:
	table = dynamodb.create_table(
    		TableName = 'Commands',
    		KeySchema = [       
        		{ 'AttributeName': 'Thermometr', 'KeyType': 'HASH' }, # //Partition key
        		{ 'AttributeName': 'Boiler', 'KeyType': 'RANGE' } # //Sort key
    		],
    		AttributeDefinitions = [       
        		{ 'AttributeName': 'Thermometr', 'AttributeType': 'S' },
        		{ 'AttributeName': 'Boiler', 'AttributeType': 'S' },
    		],
    		ProvisionedThroughput = {       
        		'ReadCapacityUnits': 5, 
        		'WriteCapacityUnits': 5
    		}
		)
	print("Table status:", table.table_status)
except Exception as e:
	print ("Exception: ",e)

