#!/usr/bin/env bash

/usr/bin/pg_dumpall > /home/ec2-user/Lambda_test/database/backup/`date "+%Y%m%d"`.sql
aws s3 cp `date "+%Y%m%d"`.sql s3://akinaga-backup/Lambda/
