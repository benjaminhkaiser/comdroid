#!/bin/bash

# Runs intentanalysis tool on an apk

LOC=$1
INSTALLDIR="/tmp/xushunyi/undergradproj/Comdroid/Comdroid-1.04"
if [ -z $1 ]
then
	echo "Correct usage: runComDroid.sh [path to apk].apk [path to output]"
	echo "Or: runComDroid.sh [path to folder with /unzip, /dedex, AndroidManifest.xml]"
	exit
elif [ ${1: -4} == ".apk" ]
then
	if [ -z $2 ]
	then
		echo "Correct usage: [path to apk].apk [path to output]"
		echo "You forgot the path to output."
		echo "I need to know where to put the results."
		exit
	elif [ ! -d "$2"/dedex ]
	then
		echo "Unpacking "$1
		unzip -qq $1 -d $2/unzip/
	#	echo "Getting the manifest file"
		cp $2/unzip/AndroidManifest.xml $2/AndroidManifest.tmp
		java -jar AXMLPrinter2.jar $2/AndroidManifest.tmp > $2/AndroidManifest.xml
		rm $2/AndroidManifest.tmp

	    #echo "Disassembling the APK file"
	    mkdir $2/dedex
	    java -jar ddx1.14.jar -o -D -r -d $2/dedex/ $2/unzip/classes.dex
		LOC=$2
	fi
elif [ ! -d "$1"/dedex ]
then
	echo "Correct usage: manperm.sh [path to apk].apk [path to output]"
	echo "Or: manperm.sh [path to folder with /unzip, /dedex, AndroidManifest.xml]"
	exit
fi

find $LOC -name "*.ddx" > $LOC/dedex/DDXFILELIST

if [ ! -d $LOC/IntentResults ]
then
	mkdir $LOC/IntentResults/
	mkdir $LOC/IntentResults/actionStats/
	mkdir $LOC/log
fi
 ./intentanalysis.rb -civ "app" $LOC/dedex $LOC/AndroidManifest.xml $LOC/IntentResults > $LOC/log/details.log
 # intentanalysis.rb -civ "app" $LOC/dedex $LOC/AndroidManifest.xml $LOC/IntentResults
