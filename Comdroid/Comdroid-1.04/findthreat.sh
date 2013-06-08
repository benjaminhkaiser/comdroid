#! /bin/bash

defaultdir="/home/xushunyi/undergradproj/apps/"
resutdir= "result"

mkdir ./resultdir

if [ -z $1 ]
then
   tgtdir=$defaultdir
else
   tgtdir=$1
fi

for file in `ls $tgtdir`
do
   fullname="$tgtdir$file"
   echo $fullname

   ./runComDroid.sh $fullname $resutdir
done
