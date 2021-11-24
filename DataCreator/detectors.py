import ipaddress
import DataCreator.set as set
from DataCreator.services import *

## Picks interested attributes from packets and saves them into a list

def Tcp(Data):
	try:

		if 'tcp.srcport' in Data and ( int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst']))  in set.tcp.keys() or int(ipaddress.ip_address(Data['ip.dst']))+int(ipaddress.ip_address(Data['ip.src'])) in set.tcp.keys() ):

			try:
				ky=int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst']))
				temp=set.tcp[ky]
			except KeyError:

				ky=int(ipaddress.ip_address(Data['ip.dst']))+int(ipaddress.ip_address(Data['ip.src']))
				temp=set.tcp[ky]
			pack_count=temp[len(temp)-1]
			pack_count=pack_count+1
			# print(pack_count)
			set.servicesQ.put([ky,Data,"tcp"])

			temp.append(Data['ip.src'])
			temp.append(Data['ip.dst'])
			temp.append(Data['tcp.flags.res'])
			temp.append(Data['tcp.flags.ns'])
			temp.append(Data['tcp.flags.cwr'])
			temp.append(Data['tcp.flags.ecn'])
			temp.append(Data['tcp.flags.urg'])
			temp.append(Data['tcp.flags.ack'])
			temp.append(Data['tcp.flags.push'])
			temp.append(Data['tcp.flags.reset'])
			temp.append(Data['tcp.flags.syn'])
			temp.append(Data['tcp.flags.fin'])
			temp.append(pack_count)

			set.tcp[ky]=temp
			set.tcp_count=set.tcp_count+1
		elif 'ip.src' in Data and 'tcp.flags.syn' in Data :
			status=[]
			pack_count=1

			status.append(Data['ip.src'])
			
			status.append(Data['ip.dst'])
			
			status.append(Data['tcp.flags.res'])
			status.append(Data['tcp.flags.ns'])
			status.append(Data['tcp.flags.cwr'])
			status.append(Data['tcp.flags.ecn'])
			status.append(Data['tcp.flags.urg'])
			status.append(Data['tcp.flags.ack'])
			status.append(Data['tcp.flags.push'])
			status.append(Data['tcp.flags.reset'])
			status.append(Data['tcp.flags.syn'])
			status.append(Data['tcp.flags.fin'])
			status.append(pack_count)
			set.tcp[int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst']))]=status
			set.servicesQ.put([int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst'])),Data,"tcp"])
			set.tcp_count=set.tcp_count+1
		else:
			set.notTCP.put(Data)
	except KeyError:
		print("KeyError:TCP")
	except AttributeError:
		print( Data)		



def Udp (Data):
	
	

	try:

		if 'udp.srcport' in Data  and ( int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst']))  in set.udp.keys() or int(ipaddress.ip_address(Data['ip.dst']))+int(ipaddress.ip_address(Data['ip.src'])) in set.udp.keys() ):
		
			try:
				ky=int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst']))
				temp=set.udp[ky]
			except KeyError:
				ky=int(ipaddress.ip_address(Data['ip.dst']))+int(ipaddress.ip_address(Data['ip.src']))
				temp=set.udp[ky]
			
			set.servicesQ.put([ky,Data,"udp"])

			
			set.udp_count=set.udp_count+1
		
		
		elif 'udp.srcport' in Data:


			status=[]
			# status.append(Data)
			status.append(Data['ip.src'])
			status.append(Data['ip.dst'])
			status.append(Data['udp.srcport'])
			status.append(Data['udp.dstport'])
			status.append(1)
			set.udp[int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst']))]=status
			set.servicesQ.put([int(ipaddress.ip_address(Data['ip.src']))+int(ipaddress.ip_address(Data['ip.dst'])),Data,"udp"])
			set.udp_count=set.udp_count+1

			
		else:

			set.notUDP.put(Data)

	except KeyError:

		if 'udp.srcport' in Data  and ( int(ipaddress.IPv6Address(Data['ipv6.src']))+int(ipaddress.IPv6Address(Data['ipv6.dst']))  in set.udp.keys() or int(ipaddress.IPv6Address(Data['ipv6.dst']))+int(ipaddress.IPv6Address(Data['ipv6.src'])) in set.udp.keys() ):
		#if 'tcp.dstport' in Data :
			try:
				ky=int(ipaddress.IPv6Address(Data['ipv6.src']))+int(ipaddress.IPv6Address(Data['ipv6.dst']))
				temp=set.udp[ky]
			except KeyError:
				ky=int(ipaddress.IPv6Address(Data['ipv6.dst']))+int(ipaddress.IPv6Address(Data['ipv6.src']))
				temp=set.udp[ky]
			# print(Data)
			
			# if temp[2]==Data['udp.dstport'] and temp[3]==Data['udp.srcport']:
				# print('Udp connection detected')
			set.servicesQ.put([ky,Data,"udp"])
			
			set.udp_count=set.udp_count+1
		# elif 'udp.srcport' in Data and 'ip.dst_host' in Data and Data['ip.src'] in set.udp.keys():
		# 	temp=set.udp[Data['ip.src']]
		# 	if temp[2]==Data['udp.srcport'] and temp[3]==Data['udp.dstport']:
		# 		count=temp[4]+1
		# 		temp[4]=count
		
		elif 'udp.srcport' in Data:
			status=[]
			status.append(Data['ipv6.src'])
			status.append(Data['ipv6.dst'])
			status.append(Data['udp.srcport'])
			status.append(Data['udp.dstport'])
			status.append(1)
			set.udp[int(ipaddress.IPv6Address(Data['ipv6.src']))+int(ipaddress.IPv6Address(Data['ipv6.dst']))]=status
			set.servicesQ.put([int(ipaddress.IPv6Address(Data['ipv6.src']))+int(ipaddress.IPv6Address(Data['ipv6.dst'])),Data,"udp"])
			
			set.udp_count=set.udp_count+1
		else:
			set.notUDP.put(Data)


def Arp (Data):

	try:


		if 'arp.src.proto_ipv4' in Data and ( int(ipaddress.ip_address(Data['arp.src.proto_ipv4']))+int(ipaddress.ip_address(Data['arp.dst.proto_ipv4']))  in set.arp.keys() or int(ipaddress.ip_address(Data['arp.dst.proto_ipv4']))+int(ipaddress.ip_address(Data['arp.src.proto_ipv4'])) in set.arp.keys() ):
			
			try:
				ky=int(ipaddress.ip_address(Data['arp.src.proto_ipv4']))+int(ipaddress.ip_address(Data['arp.dst.proto_ipv4']))
				temp=set.arp[ky]
			except KeyError:
				ky=int(ipaddress.ip_address(Data['arp.dst.proto_ipv4']))+int(ipaddress.ip_address(Data['arp.src.proto_ipv4']))
				temp=set.arp[ky]

			pack_count=temp[len(temp)-1]
			pack_count=pack_count+1
			
			temp.append(Data['arp.src.proto_ipv4'])
			temp.append(Data['arp.dst.proto_ipv4'])
			temp.append(Data['arp.src.hw_mac'])
			temp.append(Data['arp.dst.hw_mac'])
			temp.append(pack_count)
			set.servicesQ.put([ky,Data,"arp"])
			
			set.arp_count=set.arp_count+1
		elif 'arp.src.proto_ipv4' in Data :


			# print('Tcp connection initiated')
			status=[]
			pack_count=1
			# status.append('ip.src')
			status.append(Data['arp.src.proto_ipv4'])
			# status.append('ip.dst')
			status.append(Data['arp.dst.proto_ipv4'])
			# status.append('tcp.flags.syn')
			status.append(Data['arp.src.hw_mac'])
			status.append(Data['arp.dst.hw_mac'])
			
			status.append(pack_count)
			set.arp[int(ipaddress.ip_address(Data['arp.src.proto_ipv4']))+int(ipaddress.ip_address(Data['arp.dst.proto_ipv4']))]=status
			set.servicesQ.put([int(ipaddress.ip_address(Data['arp.src.proto_ipv4']))+int(ipaddress.ip_address(Data['arp.dst.proto_ipv4'])),Data,"arp"])
			set.arp_count=set.arp_count+1
		else:
			set.notARP.put(Data)
			
			
	except AttributeError:
		print( Data)		