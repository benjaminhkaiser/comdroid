#!/usr/bin/python

#
#usage ./nativetest.py [apkfile] [directory]
#
#if neither of the argument is specified, using default directory
#else run the test against the file or files under the directory
#
#

import os
import sys
import json
import re


debug = 1

def find_by_regex(cmd):
    s=os.popen(cmd).read()
    res = re.search(r"(?s)Find intent vulnerabilities\n\*+\n(.*?)Print intent summary\n", s).group(1)
    return res

def find_by_index(cmd):
    s=os.popen(cmd).read()
    sm = "Find intent vulnerabilities\n******************************************************************************************"
    em = "Print intent summary\n"
    sp = s.index(sm) + sm.__len__()
    ep = s.index(em)
    res = s[sp:ep]
    return res

def find_by_intmfile(cmd, logpath):
    cmd = cmd + " >/dev/null" if debug else 0
    os.system(cmd)
    try:
        tmpfh = open("%s/IntentResults/allWarnings" % logpath ,"r")
    except IOError:
        print "File cannnot be opened"
    buff = []
    for line in tmpfh.readlines():
            buff.append(line)
    tmpfh.close
    return buff

def find_by_intmfile2(cmd, logpath):
    cmd = cmd + " >/dev/null" if debug else 0
    os.system(cmd)
    try:
       tmpfh = open("%s/IntentResults/allWarnings" % logpath ,"r")
       buff = tmpfh.read()
       tmpfh.close()
       return buff
    except IOError as e:
      print "IO ERROR({0}:{1})".format(e.errno,e.strerror)
      return None

def find_threats(files):
    cmdpath = "/home/sx2151/undergradproj/Comdroid/Comdroid-1.04/runComDroid.sh"

    logpath = os.getcwd()+"/testresult"
    finalhash ={}
    mkdircmd = "mkdir " + logpath
    if(not os.path.exists(logpath)):
        os.system(mkdircmd)
    try:
        print files
        for file in files:
            print "\nFILE: %s" % file if debug else 0
            cmd = cmdpath + " " +file+ " " +logpath
            # res = find_by_regex(cmd)
            # res = find_by_index(cmd)
            # res = find_by_intmfile(cmd, logpath)
            res = find_by_intmfile2(cmd, logpath)
            if (os.path.exists("%s/dedex" %logpath)):
                os.system("rm -rf  %s/*" %logpath)

            if res is None:
               print "is None"
               continue
            finalhash[file] = res

        outfh = open('result.json', "w")
        print json.dump(finalhash,outfh,indent=4)

    finally:
        if (os.path.exists(logpath)):
            os.system("rm -r %s" % logpath)

directory = '/home/sx2151/undergradproj/apps/'

targets = sys.argv[1:]
if targets:
    listing = []
    for ele in targets:
        if os.path.isfile(ele):
            listing.append(ele)
        else:
            if os.path.isdir(ele):
                entries = os.listdir(ele)
                entries2 = map(lambda x: ele+x, entries)
                for v in entries2:
                    listing.append(v)
    find_threats(listing)
else:
    listing = os.listdir(directory)
    listing2 = map(lambda x: directory+x, listing)
    find_threats(listing2)
