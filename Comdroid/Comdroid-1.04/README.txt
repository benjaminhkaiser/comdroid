Readme 9/4/2012
Email questions to Erika Chin, emc@cs.berkeley.edu

REQUIREMENTS
java
ruby 1.8.7 and up

To run ComDroid from scratch (from apk to output):
./runComDroid.sh <pathToAPK>/<apkName>.apk <OutputFolder>/

To run ComDroid when you already have dedex'ed files and just want to rerun results:
./runComDroid.sh <OutputFolder>/
(You are also welcome to delete the "unzip/" folder if you are low on space.  ComDroid only relies on the dedex/ and AndroidManifest.xml)

The main output is:  IntentResults/allWarnings

If you'd like different run options, you can change the flags in the line in runComDroid.sh that has the call to intentanalysis.rb  (Flags detailed below)

COMDROID

Flags
-c, --comdroid		For ComDroid output - lists vulnerable intents and components 
-s, --stowaway		For Stowaway output - lists action strings being sent and received on a per component type granularity
-m, --measurements	More output files - lists actions being sent and received (2 files, not per component type), and explicit intent destinations

Flags that affect the log file
-v, --[no-]verbose	For details in the log file
-d, --debug		For even more details in the log file (with register values, etc.) for debugging and other debug files
-i, --intents		For Intent details in the log file


*******************ComDroid Flag Output*******************
IntentResults/allWarnings - Primary output.  Lists all Unauthorized Intent Receipt warnings (Broadcast Theft, Activity Hijacking, Service Hijacking), Intent Spoofing warnings (Malicious Broadcast Injection, Malicious Activity Launch, Malicious Service Launch), Action Misuse warnings, and Protected System Broadcast w/o action check warnings.
IntentResults/actionMisuse - subset of allWarnings file.  Only lists Action Misuse cases
IntentResults/protectedBroadcastNoAction - subset of allWarnings file.  Only lists Protected System Broadcast w/o action check cases


*******************Measurements Flag Output***************
IntentResults/actionStats/receivingActions.txt - all actions for receiving components
IntentResults/actionStats/sendingActions.txt - all actions for sending components
IntentResults/actionStats/all_setDestinations.txt - (Experimental) lists destinations for explicit intents

Debug files (appear if debug flag is on):
IntentResults/actionStats/all_setActions.txt - debugging file for all strings that go to a Intent.setAction() call or Intent constructor
IntentResults/actionStats/actionDebug - debug info on Intent actions
IntentResults/actionStats/actionFrequency - debug info.  Lists actions and the intents they came from.
IntentResults/actionStats/setActionNotFound.txt - debugging file for location of places where the action goes to Intent.setAction() call or Intent constructor and the action string could not be determined.
IntentResults/actionStats/setDestinationNotFound.txt - debugging file for location of places where the destination for explicit intents are not found
IntentResults/actionStats/sinksNotDone.txt - sinks that don't have some intent mapped to it

Internal stats (Commented out, but if you find any of this useful…):
actionMisuseCatchesWarnings - internal stats file.  Counts the number of warnings (from components and intents) that would be removed if action misuse were fixed
sinkcount - internal stats file.  Serialized data of number of startActivity, startService, sendBroadcast etc.
totalcomponents - internal stats file.  Serialized data of number of components, divided by component type, etc.
explicitcount - serialized data of number of explicit Intents and number fully resolved
vulnWODefault - activities that don't have default category


*******************Stowaway Flag Output*******************
List of the actions found separated into the files by destination|receiving component type:
	sendActivityActions.txt
	sendBroadcastActions.txt
	sendServiceActions.txt
	sendOtherActions.txt - if the destination component couldn't be determined they fall into this file

	recvActivityActions.txt
	recvReceiverActions.txt
	recvServiceActions.txt

allActions.txt - debugging file for all strings that go to a Intent.setAction() call or Intent constructor (*Note: For Intents sent, not received)
allStrings.txt - all const strings in the application (excludes xml files)

Debug files (appear if debug flag is on):
actionNotFound.txt - debugging file for location of places where the action goes to Intent.setAction() call or Intent constructor and the action string could not be determined.
otherActionLocation.txt - debugging file for intent locations of intents that fall into the sendOtherActions.txt file
