import subprocess
import os
import sys

def checkPathForADB():
	try:
		subprocess.Popen(["adb"], stderr=subprocess.STDOUT, stdout = subprocess.PIPE)
	except OSError:
		print "Make sure your $PATH environment variables includes the path to adb"
		sys.exit(0)	

def startActivity():
	activity = raw_input("Enter the name of the package and activity in the following format: \ncom.google.android.contacts/.ContactsActivity \n")
	cmd = 'adb shell am start -n ' + activity
	try:
		p = subprocess.Popen([cmd], shell = True, stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
		out, err = p.communicate()
		e = out.find("Error")
		if e is not -1:
			print out[e:]
	except OSError as e:
		print e
		sys.exit(0)

checkPathForADB()
startActivity()
print "finished"