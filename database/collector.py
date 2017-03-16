#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import boto3
import json
import sys

client = boto3.client('lambda', region_name="ap-northeast-1")

now = datetime.datetime.now()
inittime = int(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)

args = sys.argv
seq = str(args[1])
uuid = str(args[2])

response = client.invoke(
    FunctionName='Lambda_test',
    InvocationType='RequestResponse',
    Payload=json.dumps({'inittime': inittime, 'seq': seq, 'uuid': uuid})
)
res = response['Payload'].read()
print json.loads(res)
