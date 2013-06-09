#!/bin/bash

end=`expr $1 \\* 48826`
begin=`expr $end - 48825`
echo $begin
echo $end
time ./nativemt.py ../../try $(sed -n "$begin,$end p" /tmp/xushunyi/undergradproj/name.txt)
