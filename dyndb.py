from __future__ import print_function # Python 2/3 compatibility
import boto3
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr


class Tempdb:
    def __init__(self,url="http://localhost:8000",region="eu-central-1"):
    	self.dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=url)
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
        return response
#   print('put_item result:', response)
#   print('\n')

    def thermo_get_minutes(self,minutes,thermo_name="InsideHall"):
        response = self.table.query(
            KeyConditionExpression=Key('Thermometer').eq(thermo_name) &
                                        Key('GetDate').gt(get_val(time.time()-minutes*60))
            )
        return response

    


def get_val(thermo):
    return decimal.Decimal(thermo)

def get_now():
    return decimal.Decimal(time.time())



#db=Tempdb()
#db.put_values('25.5','30')
#db.put_values('35.5','30')
#db.put_values('35.5','10')
