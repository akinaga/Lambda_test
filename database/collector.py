#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import boto3
import json
import sys
import requests
import base64


client = boto3.client('lambda', region_name="ap-northeast-1")

now = datetime.datetime.now()
inittime = int(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)

args = sys.argv
seq = str(args[1])
uuid = str(args[2])
FunctionName = str(args[3])

if "Lambda_test" in FunctionName:
    response = client.invoke(
        # FunctionName='Lambda_test',
        FunctionName=FunctionName,
        # FunctionName='Lambda_test_003',
        # FunctionName='Lambda_test_004',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps({'inittime': inittime, 'seq': seq, 'uuid': uuid+" "+FunctionName})
    )
    # res = response['Payload'].read()
    res = response['LogResult']
    res2 = base64.b64decode(res)
    print res2

elif "Lambda_s3test" in FunctionName:
    bucket_name = "akinaga-lambda-test"
    json_key = str(seq) + ".txt"
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, json_key)
    txt = ""
    r = obj.put(Body=json.dumps({'inittime': inittime, 'seq': seq, 'uuid': uuid+" "+FunctionName}))

else:
    ipaddr = FunctionName
    print ipaddr
    r = requests.get("http://" + ipaddr + ":5000",
                            params={'inittime': inittime, 'seq': seq, 'uuid': uuid+" "+FunctionName})
    res = r.text

# print json.loads(res)
