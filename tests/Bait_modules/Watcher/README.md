WATCHER MODULE

Deploy.ps1 : A powershell script that once executed it triggers the installation of the watcher.ps1

Watcher.ps1: A Background powershell service that monitors a sensitive directory specified for changed made to it ie Copy,Delete, Addition or Updating
	- It used HTTP Method POST to upload the triggered event alert to the API endpoint.
	

INSTALLATION PROCESS
: powershell -ExecutionPolicy Bypass -F Path/to/Deploy.ps1


Installation Path: C:\watcher
	- The watcher.ps1 is installed in the path above named after the bait id ie C:\watcher\A123B.ps1
	- By default installation is hidden thus using dir wont show it in the listed files.
	- To Exposer the file run command : attrib -h -s C:/watcher/A123B.ps1
	


ISSUE:
	-	The Background Process doesn't start automatically it keeps a status queued
	-	To monitor the process status use the command below


	-	schtasks /query /tn "WatcherUpdate" : To list the Status of the Current status

	-	schtasks /run /tn "WatcherUpdate" : To run the Background process

	-	schtasks /Query /FO LIST /TN "WatcherUpdate" : List information related to the process

	-	schtasks /delete /tn "WatcherUpdate" /f : To Delete the Bg process
	