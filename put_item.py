from __future__ import print_function # Python 2/3 compatibility
import boto3
import decimal
import time


def get_val(thermo):
    return decimal.Decimal('25.3')

def get_now():
    return decimal.Decimal(time.time())


dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Temperature');
thermo_name="InsideHall";

for f in range(2):
    response=table.put_item(
        Item={
            'Thermometer': thermo_name,
            'GetDate': get_now(),
            'val': get_val(thermo_name),
        }
    )
    print('put_item result:', response)
