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
import thread
import threading
debug = 1
THREAD_NUM=16


def find_by_intmfile2(cmd, logpath):
    cmd = cmd + " >/dev/null" if debug else cmd
    os.system(cmd)
    try:
       tmpfh = open("%s/IntentResults/allWarnings" % logpath ,"r")
       buff = tmpfh.read()
       tmpfh.close()
       return buff
    except IOError as e:
       print "IO Error {0}:{1}".format(e.errno,e.strerror)
       return None


def find_threats(files, logpath, finalhash, finalerrhash):
    global lock
    global count
    localhash ={}
    errhash={}
    tid = threading.current_thread().name
    lock.acquire()
    print tid +":", files
    lock.release()

    r=re.compile(r"apps/(.*?).apk")
    for file in files:
         lock.acquire()
         count += 1
         print "\n%d FILE: %s" %(count, file) if debug else 0
         lock.release()

         filepostfix = r.search(file)
         logdir = logpath + filepostfix.group(1)
         cmd = "/home/sx2151/undergradproj/Comdroid/Comdroid-1.04/runComDroid.sh %s"% (logdir)
         print "The cmd is:" + cmd
         res = find_by_intmfile2(cmd, logdir)
         if res is None:
            errhash[file] = tid
            continue
         localhash[file] = res
    lock.acquire()
    finalhash.update(localhash)
    finalerrhash.update(errhash)
    lock.release()


directory = '/home/sx2151/undergradproj/apps/'
logdir = '/home/sx2151/undergradproj/log/'
targets = sys.argv[1:]
if targets:
    listing = []
    for ele in targets:
        if os.path.isfile(ele):
            listing.append(ele)
        else:
            if os.path.isdir(ele):
                if ele[-1] != '/': ele += '/'
                entries = os.listdir(ele)
                entries2 = map(lambda x: ele+x, entries)
                for v in entries2:
                    listing.append(v)
else:
    listing = os.listdir(directory)
    listing = map(lambda x: directory+x, listing)

listing_len = len(listing)
slice_size = listing_len/THREAD_NUM
lock = threading.Lock()
count=0
threads=[]
finalhash={}
finalerrhash={}
start=0
end=0
count=0
for i in range(THREAD_NUM):
   start = i*slice_size
   end = start + slice_size
   end = end if end<listing_len else listing_len
   listing_slice = listing[start:end]
   logpath = logdir
   thread = threading.Thread(target=find_threats, args=(listing_slice,logpath, finalhash, finalerrhash))
   threads.append(thread)
   thread.start()

for thread in threads:
   thread.join()

hitresult =logdir+"/result.json"
missresult = logdir+"/miss.json"
outfh = open(hitresult, "w")
print json.dump(finalhash,outfh,indent=4)
outfh.close()
errfh = open(missresult,'w')
print json.dump(finalerrhash,errfh,indent=4)
errfh.close()





