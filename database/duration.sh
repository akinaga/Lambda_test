#!/usr/bin/env bash

for i in {1..10000}
do
#    psql -d traffic -c "insert into lambda_duration values('$1', $i, $(cat result/$1/$i | grep Duration | cut -d" " -f4));"
    echo $1, $i, $(cat result/$1/$i | grep Duration | cut -d" " -f4)
done



