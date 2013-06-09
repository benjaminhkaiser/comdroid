#!/usr/bin/python

#
#usage ./nativetest.py [apkfile] [directory]
#
#if neither of the argument is specified, using default directory
#else run the test against the file or files under the directory
#
#

from optparse import OptionParser
import os
import sys
import json
import re
import thread
import threading
debug = 1
THREAD_NUM=8

#class myThread(threading.Thread):
#   def __init__(self, listing, logpath):
#      threading.Thread.__init__(self)
#      self.listing = listing
#      self.logpath = logpath
#
#   def run(self):
#       self.find_threats(self.listing, self.logpath)

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
       print "IO Error {0}:{1}".format(e.errno,e.strerror)
       return None


def find_threats(files, logpath, finalhash, finalerrhash):
    cmdpath = "/tmp/xushunyi/undergradproj/Comdroid/Comdroid-1.04/runComDroid.sh"
    global lock
    global count
    localhash ={}
    errhash={}
    mkdircmd = "mkdir " + logpath
    tid = threading.current_thread().name
    lock.acquire()
    print tid +":", files
    lock.release()

    if(not os.path.exists(logpath)):
        os.system(mkdircmd)
    try:
        for file in files:
            lock.acquire()
            count += 1
            print "\n%d FILE: %s" %(count, file) if debug else 0
            lock.release()
            cmd = cmdpath + " " +file+ " " +logpath
            # res = find_by_regex(cmd)
            # res = find_by_index(cmd)
            # res = find_by_intmfile(cmd, logpath)
            res = find_by_intmfile2(cmd, logpath)
            if (os.path.exists("%s/dedex" %logpath)):
                os.system("rm -rf  %s/*" %logpath)
            if res is None:
               errhash[file] = tid
               continue
            localhash[file] = res

        lock.acquire()
        finalhash.update(localhash)
        finalerrhash.update(errhash)
#        outfh = open('result.json', "a")
#        print threading.current_thread().name+" is writing json"
#        print json.dump(localhash,outfh,indent=4)
#        outfh.close()
#        errfh = open('err.json','a')
#        print json.dump(errhash,errfh,indent=4)
#        errfh.close()
        lock.release()

    finally:
        if (os.path.exists(logpath)):
            os.system("rm -r %s" % logpath)

parser = OptionParser()
parser.add_option("-f")
parser.add_option("-l")
(options, args) = parser.parse_args()

directory = '/tmp/xushunyi/undergradproj/apps/'
logdir = '/tmp/xushunyi/undergradproj/log/'
if options.l:
   logdir = options.l
   if logdir[-1] != '/': logdir += '/'
os.system("mkdir %s" %logdir)

if options.f:
   file = open(options.f, 'r')
   listing = file.readlines()
   listing = map(lambda s:s.strip('\n'), listing)
   file.close()
   print listing

#targets = sys.argv[2:]
#if targets:
#    listing = []
#    for ele in targets:
#        if os.path.isfile(ele):
#            listing.append(ele)
#        else:
#            if os.path.isdir(ele):
#                if ele[-1] != '/': ele += '/'
#                entries = os.listdir(ele)
#                entries2 = map(lambda x: ele+x, entries)
#                for v in entries2:
#                    listing.append(v)
#    #find_threats(listing)
#else:
#    listing = os.listdir(directory)
#    #listing2 = map(lambda x: directory+x, listing)
#    #find_threats(listing2)
#    listing = map(lambda x: directory+x, listing)

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
   listing_slice = listing[start:end]
   #logpath = os.getcwd()+"/testresult_"+str(i)
   logpath = logdir+"testresult_"+str(i)
   thread = threading.Thread(target=find_threats, args=(listing_slice,logpath,finalhash, finalerrhash))
   threads.append(thread)
   thread.start()

listing_slice = listing[end:listing_len] #deal with remainant file
#logpath = os.getcwd()+"/testresult_"+str(THREAD_NUM)
logpath = logdir+"testresult_"+str(THREAD_NUM)
thread = threading.Thread(target=find_threats, args=(listing_slice,logpath,finalhash, finalerrhash))
threads.append(thread)
thread.start()

for thread in threads:
   thread.join()

#hitresult = "/scratch/class/w4118/os018/xsy/out/result.json"
hitresult =logdir+"result.json"
missresult = logdir+"miss.json"
#missresult = "/scratch/class/w4118/os018/xsy/out/miss.json"
outfh = open(hitresult, "a")
print json.dump(finalhash,outfh,indent=4)
outfh.close()
errfh = open(missresult,'a')
print json.dump(finalerrhash,errfh,indent=4)
errfh.close()





