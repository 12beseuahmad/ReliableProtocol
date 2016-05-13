# FALL 2014 Computer Networks		SEECS NUST
# BESE 3
# Dr Nadeem Ahmed
# BadNet1: Drops every 5th Packet
# Usage: BadNet.transmit instead of sendto


from socket import *

class BadNet:

	counter = 1
	@staticmethod
	def transmit(csocket,message,serverName,serverPort):
#		print 'Got a packet' + str(BadNet.counter)
		
		if (BadNet.counter % 5) != 0:
			csocket.sendto(message,(serverName,serverPort))
			print 'BadNet Sends properly packet No ' + str(BadNet.counter)
	
		else:
			print 'BadNet Dropped a packet No ' + str(BadNet.counter)
			pass	

		BadNet.counter=BadNet.counter+1	





