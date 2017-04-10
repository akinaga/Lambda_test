#!/usr/bin/env bash

for i in 128 256 384 512 640 768 896 1024 1152 1280 1408 1536
do
    bash collector.sh Lambda_test_"$i"M
done
