import threading
import DataCreator.set as set


## check the traffic for different services in the traffic suhc as ssl,http,smtp

class services (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		global service_count
		service_count=0
		while True:

			if set.servicesQ.empty()==False:
				
				Datalist=set.servicesQ.get()
				service_count=service_count+1
				global serv
				serv =[]
				global ID
				ID=Datalist[0]
				Data=Datalist[1]
				global Prot1
				Prot1=Datalist[2]
				if Prot1=="tcp" or Prot1=="udp" :
									
					ssl(Data)
					http(Data)
					ftp(Data)
					ssh(Data)
					dns(Data)
					smtp(Data)
					dhcp(Data)
					
				if len(serv)>0:
					Datalist.append(serv)
					set.timesQ.put(Datalist)
				else:
					Datalist.append(["no service"])
					set.timesQ.put(Datalist)



				
				
				# print(ID,Data,Prot1,service_count)


# if more services are needed they can be added in the following template

def ssl(Data):
	
	if "ssl.record.content_type" in Data :
		
		serv.append("ssl")
		

def http(Data):
	
	if "http.request.method" in Data :
		
		serv.append("ssl")
		

def ftp(Data):
	
	if "ftp.request" in Data :
		serv.append("ssl")
		

def ssh(Data):
	
	if  'ssh.payload' in Data :
		serv.append("ssl")
	
	
def dns(Data):
	
	if  'dns.flags' in Data :
		serv.append("ssl")

def smtp(Data):
	if 'smtp.response' in Data :
		serv.append("ssl")

def dhcp(Data):
	if 'dhcpv6.msgtype' in Data :
		serv.append("dhcp")