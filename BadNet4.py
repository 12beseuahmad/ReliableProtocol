# FALL 2014 Computer Networks		SEECS NUST
# BESE 3
# Dr Nadeem Ahmed
# BadNet4:  Re-orders every 5th and 6th Packet
# Usage: BadNet.transmit instead of sendto


from socket import *
import time

class BadNet:

	dummy=' '
	reorder=0
	counter = 1
	@staticmethod
	def transmit(csocket,message,serverName,serverPort):
#		print 'Got a packet' + str(BadNet.counter)
		
		if (BadNet.counter % 5) != 0:
			csocket.sendto(message,(serverName,serverPort))
			print 'BadNet Sends properly packet No ' +str(BadNet.counter)
	
		else:
			print 'BadNet re-ordering a packet' + str(BadNet.counter)
			if BadNet.reorder == 1:
				csocket.sendto(message,(serverName,serverPort))
#				time.sleep(1)
				csocket.sendto(BadNet.dummy,(serverName,serverPort))
				BadNet.reorder=0
				BadNet.counter=BadNet.counter+1	
				
			else:
				BadNet.dummy=message
				BadNet.reorder=1
				BadNet.counter=BadNet.counter-1	
		
		BadNet.counter=BadNet.counter+1	





