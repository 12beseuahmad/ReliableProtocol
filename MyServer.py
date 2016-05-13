# Group Members:
# Umair Ahmad (00321)
# Nauman Haroon (01917)

from socket import *
#from BadNet0 import*									#for badnet 0
#from BadNet1 import*									#for badnet 1
#from BadNet2 import*									#for badnet 2
#from BadNet3 import*									#for badnet 3
#from BadNet4 import*									#for badnet 4
from BadNet5 import*									#for badnet 5
import hashlib										#for calculating checksum
import pickle										#for serialize and Deserialize
import sys										#for accessing commandline arguments

serverPort = int(sys.argv[1])								#setting port by commandline 
serverSocket = socket(AF_INET, SOCK_DGRAM)	
serverSocket.bind(('', serverPort))

track=[]										#List for Keeping a track of packet that have been recieved
pkt=[]											#for accessing the recieved packet
checksum_recieved=''									#Global variable in which recieved checksum will be stored on recieving
checksum_calculate=''									#Global variable for checksum that we will calulate on recieving the ACK
output=''										
recieve='false'	
sequencecheck=1;

print 'The server is ready to recieve'

while True:										#loop true untill recieve "END"
	
	try:	
		chunk, clientAddress=serverSocket.recvfrom(4096)			#recieve a packet
		pkt = pickle.loads(chunk)						#store in type list ie pkt
		checksum_recieved = pkt[-1]						#temporary store checksum
		del pkt[-1]								#delete checksum 
		checksum_calculate = hashlib.md5()				
		checksum_calculate.update(pickle.dumps(pkt))				#calculate cheksum without the recieved checksum
		recieve='true'								#shows that packets is recieved
		elseack=pkt[0]-1;
	except:			
		recieve='false'								#packet not recived or dropped
		
	if (recieve=="true" and checksum_calculate.digest()==checksum_recieved and pkt[0]==sequencecheck):	#if packet is recieved and Checksum is also correct
		sequencecheck=sequencecheck+1;		
		pkt=pickle.loads(chunk)							#deserialize into list
		print "Recieved", pkt[0]
		if pkt[0] in track:							#check if already recieved (if true then only send Ack dont store)
			ACK=[]
			ACK.append(pkt[0])
			ACK.append("ACK")
			checksum = hashlib.md5()
			checksum.update(pickle.dumps(ACK))
			ACK.append(checksum.digest())
			SACK=pickle.dumps(ACK)
			print "Sent ACK", ACK[0]
			BadNet.transmit(serverSocket,SACK,clientAddress[0],clientAddress[1])
			
		
		else:									#if is not in the track list 
			track.append(pkt[0])						#add to track list
			data=pkt[1]							#access data
			ACK=[]								#for creating ack
			ACK.append(pkt[0])						#append serial no as the serial number of the packet recieved
			ACK.append("ACK")						#append string named ACK
			checksum = hashlib.md5()			
			checksum.update(pickle.dumps(ACK))				#calculate checksum
			ACK.append(checksum.digest())					#append checksum
			SACK=pickle.dumps(ACK)						#deserialize
			BadNet.transmit(serverSocket,SACK,clientAddress[0],clientAddress[1])	#send it to the sender
			print "Sent ack", ACK[0]
			if data=="END":							#if data Recieved is "END" it means that this is the last packet
				break							#break and write all data in file
			output=output+data						#if not "END" Append that data in Output
			recieve = 'false'
	else:
		ACK=[]									#for creating ack
		ACK.append(pkt[0])							#append serial no as the serial number of the packet recieved
		ACK.append("ACK")							#append string named ACK
		checksum = hashlib.md5()			
		checksum.update(pickle.dumps(ACK))					#calculate checksum
		ACK.append(checksum.digest())						#append checksum
		SACK=pickle.dumps(ACK)							#deserialize
		BadNet.transmit(serverSocket,SACK,clientAddress[0],clientAddress[1])	#send it to the sender
		
		
f = open("recieved.pdf", "wb")					# writing recieved filedata into the destination file
f.write(output)
f.close()
	
print '\nFile recieved Succesfully, Check current Working Directory'	
		
		
print "CONNECTION CLOSED"
serverSocket.close()
	


	









