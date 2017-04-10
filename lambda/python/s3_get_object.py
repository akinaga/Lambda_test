from __future__ import print_function

import urllib
import boto3
import time
import datetime

print('Loading function')

s3 = boto3.client('s3')
queueName = 'Lambda_test'


def lambda_handler(event, context):
    now = datetime.datetime.now()
    opentime = int(time.mktime(now.timetuple()) * 1000 + now.microsecond / 1000)

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        # return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    body = response['Body'].read()
    print(body)
    import json
    dat = json.loads(body)
    uuid = dat['uuid']
    seq = dat['seq']
    inittime = int(dat['inittime'])

    difftime = opentime - inittime

    dat = {}
    dat['seq'] = seq
    dat['opentime'] = opentime
    dat['inittime'] = inittime
    dat['uuid'] = uuid
    dat['difftime'] = difftime

    session = boto3.session.Session(region_name='ap-northeast-1')
    sqs = session.resource('sqs')
    response = sqs.get_queue_by_name(QueueName=queueName).send_message(MessageBody=json.dumps(dat))

    return json.dumps(dat)

