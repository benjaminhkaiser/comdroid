import subprocess
import os
import sys

#Types are "Activity" "Service" or "Broadcast"
class Vuln:
	def __init__(self, vs):
		self.vulnString = vs

		#parse Malicious Activity Launch vulns
		t = vs.find("Malicious Activity Launch")
		c = vs.find(",")
		if t is not -1:
			self.type = "Activity"
			self.activity = vs[t+27:c]
			self.line = vs[c+2:]
			return

		#parse Malicious Broadcast Injection vulns
		t = vs.find("Malicious Broadcast Injection")
		c = vs.find(",")
		if t is not -1:
			self.type = "Broadcast"
			self.activity = vs[t+31:c]
			self.line = vs[c+2:]

	def __str__(self):
		try:
			return("Type: " + self.type + "\nActivity: " + self.activity + "\nLine: " + self.line)
		except:
			return(self.vulnString)

def checkPathForADB():
	try:
		subprocess.call(["adb"], stderr=subprocess.STDOUT, stdout = subprocess.PIPE)
	except OSError:
		print "Make sure your $PATH environment variables includes the path to adb."
		sys.exit(0)	

def startActivity():
	activity = raw_input("Enter the name of the package and activity in the following format: " + 
		                 "\ncom.google.android.contacts/.ContactsActivity \n")
	cmd = 'adb shell am start -n ' + activity
	try:
		p = subprocess.call([cmd], shell = True, stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
		out, err = p.communicate()
		e = out.find("Error")
		if e is not -1:
			print out[e:]
	except OSError as e:
		print e
		sys.exit(0)

def runComDroidScan():
	apk = raw_input("Enter the path to the apk you want to spoof.\n").rstrip()
	output = raw_input("Enter the path to the directory where you want output to be stored.\n").rstrip()

	try:
		subprocess.call(["./runComDroid.sh "+apk+" "+output], shell=True,
						 stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
	except OSError as e:
		print e
		sys.exit(0)

	#TODO: better output file handling
	outputFile = open(output+"/IntentResults/allWarnings", 'r')
	spoofVulns = []
	for line in outputFile:
		if "Malicious" in line:
			spoofVulns.append(Vuln(line))

	if len(spoofVulns) == 0:
		print "No intent spoofing vulnerabilities found. See "+ output+"/IntentResults/allWarnings for full scan output."
	else:
		print str(len(spoofVulns)) + " intent spoofing vulnerabilities found."
		exploitVulns(spoofVulns)

def exploitVulns(spoofVulns):
	for i in range(len(spoofVulns)):
		print "Vulnerability " + str(i) + ":"
		print spoofVulns[i]


checkPathForADB()
runComDroidScan()
