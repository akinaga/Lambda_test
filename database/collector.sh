#!/bin/bash -f

uuid=$(uuidgen)
mkdir result/$uuid
echo "$1 -> $uuid"

echo ---- Start Lambda Testing---
for i in {1..10000}
do
	#echo "Target: $i is processing"
    python collector.py $i $uuid $1 > result/$uuid/$i &
	while :
	do
	    v=$(ps ax | grep collector.py | grep -v grep | wc -l)
		printf '\r %s:%s:%s  ' $i $v $(seq -s= $v|tr -d '[:digit:]')
		if [ $(ps ax | grep collector.py | grep -v grep | wc -l) -le 100 ]; then
			break
        else
            sleep 0.1
		fi
	done
done

# waiting for processing
while :
do
    sleep 0.5
    echo $(ps ax | grep collector.py | grep -v grep | wc -l)
    if [ $(ps ax | grep collector.py | grep -v grep | wc -l) -le 0 ]; then
        break
    fi
done

printf '\n'