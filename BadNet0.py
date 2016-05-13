# FALL 2014 Computer Networks		SEECS NUST
# BESE 3
# Dr Nadeem Ahmed
# Good Net ;)
# Usage: BadNet.transmit instead of sendto


from socket import *

class BadNet:
	counter=1
	@staticmethod
	def transmit(csocket,message,serverName,serverPort):
		csocket.sendto(message,(serverName,serverPort))
		print 'BadNet Sends properly packet No ' + str(BadNet.counter)
		BadNet.counter=BadNet.counter+1

