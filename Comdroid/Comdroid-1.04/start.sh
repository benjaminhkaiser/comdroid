#!/bin/bash

#end=`expr $1 \\* 48826`
#begin=`expr $end - 48825`
log="log$1"
echo $begin
echo $end
echo $log
time ./nativemt.py ../../$log $(sed -n "$begin,$end p" /tmp/xushunyi/undergradproj/name.txt)
