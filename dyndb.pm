from __future__ import print_function # Python 2/3 compatibility
import boto3
import decimal
import time


class Tempdb:
    def __init__(self,url="http://localhost:8000"):
    	self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url=url)
    	self.table = self.dynamodb.Table('Temperature');

    def put_values(self,temperature,humidity,thermo_name="InsideHall"):
   	response=self.table.put_item(
        	Item={
            		'Thermometer': thermo_name,
            		'GetDate': get_now(),
            		'val': get_val(temperature),
            		'hum': get_val(humidity),
        	}
    	)
   	print('put_item result:', response)
   	print('\n')


def get_val(thermo):
    return decimal.Decimal(thermo)

def get_now():
    return decimal.Decimal(time.time())



db=Tempdb()
db.put_values('25.5','30')
db.put_values('35.5','30')
db.put_values('35.5','10')
