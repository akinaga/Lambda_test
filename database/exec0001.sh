#!/usr/bin/env bash

for i in Lambda_test_001 Lambda_test_002 Lambda_test_003 Lambda_test_004 Lambda_test_005
do
    bash collector.sh $i
done
