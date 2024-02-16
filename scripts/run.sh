#!/bin/bash
NUMBER=20

for i in $(seq 1 $NUMBER); do
    INST=inst$i
    rm -rf $INST
    mkdir $INST
    cd $INST
    mkdir log
    mkdir log/script
    cp ../test.py .
    python3 test.py ../site/website$i >py_log.log &
    cd ..
done
wait
