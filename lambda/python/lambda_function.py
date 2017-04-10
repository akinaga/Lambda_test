#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime

queueName = 'Lambda_test'

def lambda_handler(event, context):
    now = datetime.datetime.now()
    opentime = int(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)

    inittime = event['inittime']
    uuid = event['uuid']
    seq = int(event['seq'])

    difftime = opentime - inittime

    dat = {}
    dat['seq'] = seq
    dat['opentime'] = opentime
    dat['inittime'] = inittime
    dat['uuid'] = uuid
    dat['difftime'] = difftime

    import boto3
    import json
    session = boto3.session.Session(region_name='ap-northeast-1')
    sqs = session.resource('sqs')
    response = sqs.get_queue_by_name(QueueName=queueName).send_message(MessageBody=json.dumps(dat))

    return json.dumps(dat)
