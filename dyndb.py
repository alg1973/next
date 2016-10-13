from __future__ import print_function # Python 2/3 compatibility
import boto3
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr


class Tempdb:
    def __init__(self,url="http://localhost:8000",region="eu-central-1"):
    	self.dynamodb = boto3.resource('dynamodb', region_name=region, 
					endpoint_url=url)
    	self.table_log = self.dynamodb.Table('Temperature')
        self.table_cmd = self.dynamodb.Table('Commands')

    def put_values(self,temperature,humidity,thermo_name="InsideHall",target_t=100,is_heating=0):
         try:
   		response=self.table_log.put_item(
        		Item={
            			'Thermometer': thermo_name,
            			'GetDate': get_now(),
            			'val': get_val(temperature),
            			'hum': get_val(humidity),
            			'target': get_val(target_t),
            			'heating': get_val(is_heating),
        		}
    		)
         except decimal.Inexact:
		response=self.table_log.put_item(
                        Item={
                                'Thermometer': thermo_name,
                                'GetDate': get_now(),
                                'val': float_to_decimal(temperature),
                                'hum': float_to_decimal(humidity),
            			'target': float_to_decimal(target_t),
            			'heating': get_val(int(is_heating)),
                        }
                ) 
         return response

    def thermo_get_minutes(self,minutes,thermo_name="InsideHall"):
        response = self.table_log.query(
            KeyConditionExpression=Key('Thermometer').eq(thermo_name) &
                                   Key('GetDate').gt(get_val(time.time()-
							minutes*60))
            )
        return response
    def thermo_cmd(self,target,heating,boiler_name="InsideHall",thermo_name="InsideHall"):
        response = self.table_cmd.update_item(
            Key={
                'Thermometr': thermo_name,
                'Boiler': boiler_name
                },
                UpdateExpression="set target = :t, heating=:h, utime=:u",
                ExpressionAttributeValues={
                    ':t': float_to_decimal(target),
                    ':h': get_val(heating),
                    ':u': get_now()
                },
                ReturnValues="UPDATED_NEW"
            )
        return response
    
    def get_cmd(self,boiler_name="InsideHall",thermo_name="InsideHall"):
        response = self.table_cmd.get_item(
            Key={
                'Thermometr': thermo_name,
                'Boiler': boiler_name
                }
            )
        return response

    


def get_val(thermo):
    return decimal.Decimal(thermo)

def get_now():
    return decimal.Decimal(time.time())


def float_to_decimal(float_value):
    """
    Convert a floating point value to a decimal that DynamoDB can store,
    and allow rounding.
    """
    # Perform the conversion using a copy of the decimal context that boto3
    # uses. Doing so causes this routine to preserve as much precision as
    # boto3 will allow.
    with decimal.localcontext(boto3.dynamodb.types.DYNAMODB_CONTEXT) as \
         decimalcontext:

        # Allow rounding.
        decimalcontext.traps[decimal.Inexact] = 0
        decimalcontext.traps[decimal.Rounded] = 0
        decimal_value = decimalcontext.create_decimal_from_float(float_value)

        return decimal_value

#db=Tempdb()
#db.put_values('25.5','30')
#db.put_values('35.5','30')
#db.put_values('35.5','10')
