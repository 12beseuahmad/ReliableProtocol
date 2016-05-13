# FALL 2014 Computer Networks		SEECS NUST
# BESE 3
# Dr Nadeem Ahmed
# BadNet3:  Duplicates every 5th Packet
# Usage: BadNet.transmit instead of sendto


from socket import *
import time

class BadNet:

	counter = 1
	@staticmethod
	def transmit(csocket,message,serverName,serverPort):
#		print 'Got a packet' + str(BadNet.counter)
		
		if (BadNet.counter % 5) != 0:
			csocket.sendto(message,(serverName,serverPort))
			print 'BadNet Sends properly packet No ' +str(BadNet.counter)
	
		else:
			print 'BadNet Duplicated a packet ' + str(BadNet.counter)
			csocket.sendto(message,(serverName,serverPort))

#			Wait for 1 sec and send another copy	
#			time.sleep(1)
			csocket.sendto(message,(serverName,serverPort))

		BadNet.counter=BadNet.counter+1	





