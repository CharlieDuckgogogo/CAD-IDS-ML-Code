from queue import *


global packet_count
packet_count=0
global tcp_count
tcp_count=0
global udp_count
udp_count=0
global arp_count
arp_count=0

global allkeyval
allkeyval={}

global sharedQ
sharedQ=Queue()

global notTCP
notTCP=Queue() 

global notUDP
notUDP=Queue() 

global notARP
notARP=Queue() 

global tcp
tcp={}

global tcpQ
tcpQ=Queue()

global udp
udp={}

global udpQ
udpQ=Queue()

global arp
arp={}

global arpQ
arpQ=Queue()

global servicesQ
servicesQ=Queue()

global timesQ
timesQ=Queue()

global timed
timed=Queue()

global Dataset
Dataset={}

global starting
starting=0

global howlong
howlong=6000000