import posix
import threading
import subprocess
import json
from queue import *
import ipaddress
import DataCreator.set as set
from DataCreator.detectors import *
from DataCreator.services import *
from DataCreator.counts import *
from threading import Timer

set.tcp_count=0
set.udp_count=0
set.packet_count=0



## capture packets using wireshark and convert them to python dictionary objects
class packetcap (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		cmd ="sudo -S tshark -V -l -T json"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, shell=True, universal_newlines=True)
		json_str = ""
		Temp= ""
		for line  in p.stdout:
			if line.strip() == '[': # skip the "["
				continue

			#if line.strip() in [',', ']']:
			if line.strip() == "{" and Temp == "}," or line.strip() =="]": #when catch the end of json, process the json
				json_str=json_str.strip() #erase the blankspace
				if json_str[0] !="{":
					json_str="{"+json_str
				json_str=json_str[:-1] #rarse the last comma
				json_obj = json.loads(json_str.strip())
				source_filter = json_obj['_source']['layers']
				keyval=source_filter.items()
				set.allkeyval={}
				a=unwrap(keyval,{})
				json_str = ""
				send_data(a) #send the
			else:
				json_str += line
			Temp = line.strip() #save the last line to determine the end of json

		p.stdout.close() #end loop
		p.wait()


## separate out tcp,udp and arp traffic

class packetanalyze (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		while True:
			if set.sharedQ.empty()==False:
				fortcp=set.sharedQ.get()
				Data=fortcp
				Tcp(Data)
			if set.notTCP.empty()==False:
				forudp=set.notTCP.get()
				Udp(forudp)
			if set.notUDP.empty()==False:
				forarp=set.notUDP.get()
				Arp(forarp)


## saves each dictionary object into a Queue

def send_data(dictionary):
	set.packet_count =set.packet_count+1
	# if set.packet_count < 50000:
	set.sharedQ.put(dictionary)


## this function unwraps a multi level JSON object into a python dictionary with key value pairs

def unwrap(keyval,temp):
	for key1,value1 in keyval:
		if type(value1)== str :
			temp[key1]=value1
		else:
			unwrap(value1.items(),temp)
	return(temp)


## start the service threads

datacollect = packetcap (1, 'packet capture data')
datacollect.start()

dataprocess = packetanalyze (2,'packet analyzing thread')
dataprocess.start()

dataservices =  services (3 ,'service analyzing thread')
dataservices.start()

timecounts =  times (4 ,'time the packets')
timecounts.start()

