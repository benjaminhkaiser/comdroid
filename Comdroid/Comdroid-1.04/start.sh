#!/bin/bash

end=`expr $1 \\* 48826`
begin=`expr $end - 48825`
log="log$1"
part="part$1"
echo $begin
echo $end
echo $log
echo $part
#time ./nativemt.py ../../$log $(sed -n "$begin,$end p" /tmp/xushunyi/undergradproj/name.txt)

sed -n "$begin,$end p" /tmp/xushunyi/undergradproj/name.txt > "$part"
time ./nativemt.py -l ../../$log -f $part
