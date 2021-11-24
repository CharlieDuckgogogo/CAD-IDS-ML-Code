import threading
import DataCreator.set as set
import math
import DataCreator.cvar as cvar
import csv



## Divide the data into time windows so that you can get average information for a given time

class times (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.current_time=0
		
		
	def run(self):

		with open('dataset.csv', 'w') as csvfile:
			fieldnames = ['tcp_frame_length', 'tcp_ip_length','tcp_length','udp_frame_length', \
				'udp_ip_length','udp_length','arp_frame_length','src_length','dst_length','num_ssl', \
				'num_http','num_ftp','num_ssh','num_smtp','num_dhcp','num_dns','num_tcp', \
				'num_udp','num_arp','connection_pairs','num_ports','num_packets']

			global writer
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			

			global pack_count
			pack_count=0
			global time_window
			time_window=5000
			global time_count
			time_count=0
			global time_window_stop
			time_window_stop=0

			while self.current_time<set.starting+set.howlong:

				if not set.timesQ.empty():

					pack_count=pack_count+1
					Datalist=set.timesQ.get()

					global ID
					ID=Datalist[0]
					Data=Datalist[1]
					global Prot1
					Prot1=Datalist[2]
					global services
					services=Datalist[3]
					global timec
					timec=0
					if pack_count==1:

						time_count=time_count+1

						full_time=Data['frame.time_epoch']
						full_time=int(float(full_time)*1000)
						timestamp=(full_time)
						set.starting=timestamp
						set.current_time=timestamp

						time_window_start_ceil=timestamp
						time_window_stop=time_window_start_ceil+time_window

					rec=timecheck(Data,time_window_stop,time_count,timec)
					self.current_time=rec[2]
					time_window_stop=rec[1]
					time_count=rec[0]
					timec=rec[0]
					calculate(ID,Data,Prot1,services,timec,writer)








def timecheck(Data,time_window_stop,time_count,timec):



	full_time=Data['frame.time_epoch']
	full_time=int(float(full_time)*1000)
	timestamp=(full_time)

	if timestamp<=time_window_stop:
		
		timec=time_count
	else:
		time_count=time_count+1
		time_window_start_ceil=timestamp

		time_window_stop=time_window_start_ceil+time_window
		timec=time_count

	return(timec,time_window_stop,timestamp)


def calculate(ID,Data,Prot1,services,t,writer):


	# Adding or changing attributes
	
	if t==cvar.instance:

		cvar.tot_pack=cvar.tot_pack+1

		if Prot1== 'tcp':
			cvar.tcp_frame_length=cvar.tcp_frame_length+int(Data['frame.len'])
			cvar.tcp_ip_length=cvar.tcp_ip_length+int(Data['ip.len'])
			cvar.tcp_length=cvar.tcp_length+int(Data['tcp.len'])
			get_services(services)
			cvar.tcp=cvar.tcp+1
			check_ID(ID)
			ports([Data['tcp.srcport'],Data['tcp.dstport']])

		elif Prot1 == 'udp':
			cvar.udp_frame_length=cvar.udp_frame_length+int(Data['frame.len'])
			try:
				cvar.udp_ip_length=cvar.udp_ip_length+int(Data['ip.len'])
			except KeyError:
				cvar.udp_ip_length=cvar.udp_ip_length+0
			cvar.udp_length=cvar.udp_length+int(Data['udp.length'])
			get_services(services)
			cvar.udp=cvar.udp+1
			check_ID(ID)
			ports([Data['udp.srcport'],Data['udp.dstport']])

		elif Prot1 == 'arp':
			cvar.arp_frame_length=cvar.arp_frame_length+int(Data['frame.len'])
			cvar.arp=cvar.arp+1
			check_ID(ID)




	else:

		#save the attributes to a dictionary

		cvar.localdat['tcp_frame_length']=cvar.tcp_frame_length
		cvar.localdat['tcp_ip_length']=cvar.tcp_ip_length
		cvar.localdat['tcp_length']=cvar.tcp_length

		cvar.localdat['udp_frame_length']=cvar.udp_frame_length
		cvar.localdat['udp_ip_length']=cvar.udp_ip_length
		cvar.localdat['udp_length']=cvar.udp_length


		cvar.localdat['arp_frame_length']=cvar.arp_frame_length

		cvar.localdat['src_length']=cvar.udp_ip_length
		cvar.localdat['dst_length']=cvar.udp_length

		cvar.localdat['num_ssl']=cvar.ssl
		cvar.localdat['num_http']=cvar.http
		cvar.localdat['num_ftp']=cvar.ftp
		cvar.localdat['num_ssh']=cvar.ssh
		cvar.localdat['num_smtp']=cvar.smtp
		cvar.localdat['num_dhcp']=cvar.dhcp
		cvar.localdat['num_dns']=cvar.dns


		cvar.localdat['num_tcp']=cvar.tcp
		cvar.localdat['num_udp']=cvar.udp
		cvar.localdat['num_arp']=cvar.arp
		cvar.localdat['connection_pairs']=len(cvar.IDs)
		cvar.localdat['num_ports']=len(cvar.ports)
		cvar.localdat['num_packets']=cvar.tot_pack

		#add the ips

		#clear variables for the next time window

		cvar.tcp=0
		cvar.udp=0
		cvar.arp=0

		cvar.ssl=0
		cvar.http=0
		cvar.ftp=0
		cvar.ssh=0
		cvar.dns=0
		cvar.smtp=0
		cvar.dhcp=0

		cvar.IDs=[]
		cvar.ports=[]
		cvar.tot_pack=1

		cvar.tcp_frame_length=0
		cvar.tcp_ip_length=0
		cvar.tcp_length=0

		cvar.udp_frame_length=0
		cvar.udp_ip_length=0
		cvar.udp_length=0

		cvar.arp_frame_length=0
		#wite to CSV
		print("localdat")
		print(cvar.localdat)
		writer.writerow(cvar.localdat)
		set.Dataset[cvar.instance]=cvar.localdat
		cvar.instance=cvar.instance+1


		if Prot1== 'tcp':
			cvar.tcp_frame_length=cvar.tcp_frame_length+int(Data['frame.len'])
			cvar.tcp_ip_length=cvar.tcp_ip_length+int(Data['ip.len'])
			cvar.tcp_length=cvar.tcp_length+int(Data['tcp.len'])
			cvar.src_length=cvar.src_length+int(Data['tcp.len'])
			get_services(services)
			cvar.tcp=cvar.tcp+1
			check_ID(ID)
			ports([Data['tcp.srcport'],Data['tcp.dstport']])

		elif Prot1 == 'udp':
			cvar.udp_frame_length=cvar.udp_frame_length+int(Data['frame.len'])
			try:
				cvar.udp_ip_length=cvar.udp_ip_length+int(Data['ip.len'])
			except KeyError:
				cvar.udp_ip_length=cvar.udp_ip_length+0
			cvar.udp_length=cvar.udp_length+int(Data['udp.length'])
			get_services(services)
			cvar.udp=cvar.udp+1
			check_ID(ID)
			ports([Data['udp.srcport'],Data['udp.dstport']])

		elif Prot1 == 'arp':
			cvar.arp_frame_length=cvar.arp_frame_length+int(Data['frame.len'])
			cvar.arp=cvar.arp+1
			check_ID(ID)



		cvar.localdat={}
		#print("*****************************************")
		#print(set.Dataset)
		


def get_services(slist):


	if 'ssl' in slist:
		cvar.ssl=cvar.ssl+1
	elif 'http' in slist:
		cvar.http=cvar.http+1
	elif 'ftp' in slist:
		cvar.ftp=cvar.ftp+1
	elif 'ssh' in slist:
		cvar.ssh=cvar.ssh+1
	elif 'dns' in slist:
		cvar.dns=cvar.dns+1
	elif 'smtp' in slist:
		cvar.smtp=cvar.smtp+1
	elif 'dhcp' in slist:
		cvar.dhcp=cvar.dhcp+1


def check_ID(ID):
	if not ID in cvar.IDs:
		cvar.IDs.append(ID)


def ports(port):
	for p in port:

		if not p in cvar.ports:
			cvar.ports.append(p)


