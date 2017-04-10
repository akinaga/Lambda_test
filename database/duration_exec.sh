#!/usr/bin/env bash

for i in $(cat uuidlist)
do
    bash duration.sh $i
done
