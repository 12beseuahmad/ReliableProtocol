# FALL 2014 Computer Networks		SEECS NUST
# BESE 3
# Dr Nadeem Ahmed
# BadNet2:  Errors every 5th Packet
# Usage: BadNet.transmit instead of sendto


from socket import *

class BadNet:

	dummy=' '
	counter = 1
	@staticmethod
	def transmit(csocket,message,serverName,serverPort):
#		print 'Got a packet' + str(BadNet.counter)
		
		if (BadNet.counter % 5) != 0:
			csocket.sendto(message,(serverName,serverPort))
			print 'BadNet Sends properly packet No ' + str(BadNet.counter)
	
		else:
			print 'BadNet creating packet errors packet No ' + str(BadNet.counter)
			
			mylist=list(message)
#			get last char of the string			
			x=ord(mylist[-1])
			if (x&1)==1:
				#if first bit set, unset it
				x &= ~(1)
			else:
				#if first bit not set, set it
				x |=  1
			
			mylist[-1]=chr(x)
			dummy=''.join(mylist)

			csocket.sendto(dummy,(serverName,serverPort))


		BadNet.counter=BadNet.counter+1	





