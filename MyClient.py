# Group Members:
# Umair Ahmad (00321)
# Nauman Haroon (01917)

from socket import*							
#from BadNet0 import*					#For BadNet 0
#from BadNet1 import*					#For BadNet 1
#from BadNet2 import*					#For BadNet 2
#from BadNet3 import*					#For BadNet 3
#from BadNet4 import*					#For BadNet 4
from BadNet5 import*					#For BadNet 5
import hashlib						#For Calculating CheckSum
import pickle						#For Serializing and Deserializing
import time						#For Timeout
import sys						#for accessing Commandline Arguments


serverIP = '127.0.0.1'
serverPort = int(sys.argv[1])				#Port Set using CommandLine Argument
clientSocket=socket(AF_INET,SOCK_DGRAM) 
clientSocket.settimeout(0.1)				#Setiing Socket Timeout 

filename=sys.argv[2]					#Filename set using CommandLine Argument 
pktlist=[]						#This is a List in which All packets are Stored Each packet itself is stored as a list
DACK=[]							#This is used to store the Ack recieved
pksnd=[]						#storing purpose
sn=1							#sequence No initialized to 1
checksum_calculate=''					#Global variable for checksum that we will calulate on recieving the ACK
checksum_recieved=''					#Global variable in which recieved checksum will be stored on recieving
ack='false'						#For checking conditions
sequencecheck=1


fileOpen = open(filename, 'rb')				#Opening file which we want to send in readbinary mode 
chunk=fileOpen.read(500)				#reading chunk of data
while chunk:						#while there is data left in the file 
	pkt=[]						#create Packet
	pkt.append(sn)					#append sequence no
	pkt.append(chunk)				#append chunk that we have read			
	pktlist.append(pkt)				#append this packet in the List of Packets
	sn=sn+1
	chunk=fileOpen.read(500)

fileOpen.close()
pktlist.append([sn,"END"])				#Append END to ensure the Reciever that file is Completely recieved on recieving END
sn=sn+1

starttime = time.time()

while pktlist:						#While there Exists a Packet in the List
 
	pksnd = pktlist[0]				#retrive a packet
	checksum = hashlib.md5()			
	checksum.update(pickle.dumps(pksnd))		#calculate Checksum
	pksnd.append(checksum.digest())			#append Checksum with that Packet
	serialized_pkt = pickle.dumps(pksnd)		
	#print "Tranmit packet", pksnd[0]	
	BadNet.transmit(clientSocket,serialized_pkt,serverIP,serverPort)	# Send that Packet
	try:									
		ACK, address = clientSocket.recvfrom(4096)			#wait for an ACK untill Time Out
		DACK = pickle.loads(ACK)					#recieve ACK
		checksum_recieved = DACK[-1]					#temporary store Checksum
		del DACK[-1]							#delete Checksum
		checksum_calculate = hashlib.md5()				
		checksum_calculate.update(pickle.dumps(DACK))			#calculate checksum after removing Checksum
		ack='true'							#AcK has Recieved 
		
	except Exception as msg:						#if timeout
		ack='false'							#ACK not recieved
		print msg							
	if (ack=='true' and checksum_calculate.digest()==checksum_recieved and DACK[0]==sequencecheck):	#IF ACK recieved and Checksum is Correct
		sequencecheck=sequencecheck+1		
		del pktlist[0]							#Delete that Packet from the Packet List and Proceed to Next in the list
		#print "received ack for", pickle.loads(ACK)[0]			
		
	else:	
										#IF ACK NOT recieved and Checksum is NOT Correct
		#print "ack not received resend packet"				#do nothing and resend the same packet 
		continue

print time.time()-starttime		
print "FIle sent Successfully"		
print "\nCONNECTION CLOSED\n"     		
clientSocket.close()

