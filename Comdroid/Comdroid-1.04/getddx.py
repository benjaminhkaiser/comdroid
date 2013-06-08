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
import multiprocessing
debug = 1
THREAD_NUM=6


def gen_ddx(files, logpath):
    cmdpath = "/home/sx2151/undergradproj/Comdroid/Comdroid-1.04/genDDX.sh"
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
         filedir = logpath + filepostfix.group(1)
         mkdircmd = "mkdir " + filedir
         if(not os.path.exists(filedir)):
               os.system(mkdircmd)
         cmd = cmdpath + " " +file+ " " +filedir
         cmd = cmd + " >/dev/null" if debug else 0
         os.system(cmd)

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
                if ele[-1]!='/': ele+='/'
                entries = os.listdir(ele)
                entries2 = map(lambda x: ele+x, entries)
                for v in entries2:
                    listing.append(v)
else:
    listing = os.listdir(directory)
    listing = map(lambda x: directory+x, listing)

listing_len = len(listing)
slice_size = listing_len/THREAD_NUM
count=0
start=0
end=0
count=0

#lock = threading.Lock()
#threads=[]
#if slice_size==0:
#   gen_ddx(listing, logdir)
#   sys.exit(0)
#
#for i in range(THREAD_NUM):
#   start = i*slice_size
#   end = start + slice_size
#   end = end if end<listing_len else listing_len
#   listing_slice = listing[start:end]
#   logpath = logdir
#   thread = threading.Thread(target=gen_ddx, args=(listing_slice,logpath))
#   threads.append(thread)
#   thread.start()
#
#for thread in threads:
#   thread.join()

lock = multiprocessing.Lock()
processes = []
if slice_size==0:
   gen_ddx(listing, logdir)
   sys.exit(0)

for i in range(THREAD_NUM):
   start = i*slice_size
   end = start + slice_size
   end = end if end<listing_len else listing_len
   listing_slice = listing[start:end]
   logpath = logdir
   ps = multiprocessing.Process(target=gen_ddx, args=(listing_slice,logpath))
   processes.append(ps)
   ps.start()

for ps in processes:
   ps.join()



