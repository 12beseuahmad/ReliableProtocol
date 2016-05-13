# FALL 2014 Computer Networks		SEECS NUST
# BESE 3
# Dr Nadeem Ahmed
# BadNet5:  a mix of drops, duplicates, errors and re-ordering of packets
# 5th dropped, 10th re-ordered, 15th duplicated, 20th errored.....
# Usage: BadNet.transmit instead of sendto


from socket import *
import time

class BadNet:

	dummy=' '
	reorder=0
	counter = 1
	error=1
	@staticmethod
	def transmit(csocket,message,serverName,serverPort):
#		print 'Got a packet' + str(BadNet.counter)
		
		if (BadNet.counter % 5) != 0:
			csocket.sendto(message,(serverName,serverPort))
			print 'BadNet Sends properly packet No ' + str(BadNet.counter)
	
		else:

			if BadNet.error==1:
				print 'BadNet Dropped a packet No ' + str(BadNet.counter)
				BadNet.error=2				
				

			elif BadNet.error==2:
				if BadNet.reorder == 1:
					print 'BadNet re-ordering a packet No ' + str(BadNet.counter)
					csocket.sendto(message,(serverName,serverPort))
#				time.sleep(1)
					csocket.sendto(BadNet.dummy,(serverName,serverPort))
					BadNet.reorder=0
					BadNet.counter=BadNet.counter+1	
					BadNet.error=3
				else:
					BadNet.dummy=message
					BadNet.reorder=1
					BadNet.counter=BadNet.counter-1	



			elif BadNet.error==3:
				print 'BadNet Duplicated a packet No ' + str(BadNet.counter)
				csocket.sendto(message,(serverName,serverPort))

				csocket.sendto(message,(serverName,serverPort))
				BadNet.error=4


			elif BadNet.error==4:
				print 'BadNet creating packet errors packet No ' + str(BadNet.counter)
			
				mylist=list(message)
#				get last char of the string			
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
				BadNet.error=1

		BadNet.counter=BadNet.counter+1	





