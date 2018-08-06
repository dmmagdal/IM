# Diego Magdaleno
# Tutorial on how to create a simple python server
# Tutorial on how to create a simple python chat server
# Tutorial on how to create a simple python p2p chat server

import socket
import threading
import sys

class Server:
		
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# AF_INET means using ipv4 (vs ipv6)
	# SOCK_STREAM means using a TCP connection
	# To have a UTP connection, replace SOCK_STREAM with SOCK_DGRAM

	connections = []
	# An empty list of connections

	def __init__(self):
		# Simple constructor
		self.sock.bind(("0.0.0.0", 10000))
		# Bind socket to an address and port
		# Parentheses is python toggle
		# First parameter in parenthesis is address
		# Second parameter in parnethesis is port
		# "0.0.0.0" was chosen to make it available to any ip address 
		# 	available on the server
		# Port 10000 was just chosen arbitrarily

		self.sock.listen(25)
		# Listen
		# Pass in the number of connections we want to allow

	def handler(self, c, a):
		# By handling the connection we're going to recieve data
		# 	from the connection
		global connections
		# A global variable to give us access to the connections list
		while True:
			data = c.recv(1024)
			# c is the connection and the max amount of data we can
			# 	recieve is 1024 bytes
			# The recv() is a blocking function which means the loop 
			# 	won't run until we actually recieve some data
			for connection in self.connections:
				# For loop to send the data back to (every) user
				connection.send(bytes(data))
				# Can only send raw bytes so pass data in bytes to 
				# 	convert the data from string to bytes
			if not data:
				print(str(a[0]) + ":" + str(a[1]) + "disconnected")
				self.connections.remove(c)
				c.close()
				# Close connection
				break
				# Allows to break out of loop

	def run(self):
		while True:
			# Create loop to handle connections
			c, a = self.sock.accept()
			# Accepts the connection
			# The connection returned is c
			# The connection's address is a
			cThread = threading.Thread(target = self.handler, args = (c,a))
			# After accepting a connection, we'll create a new thread
			# Pass in the name of the function that is going to run
			# 	once we run the thread
			cThread.daemon = True
			# Set this to true so that the program can exit regardless of
			# 	if there are any threads still running
			cThread.start()
			# Start the thread
			self.connections.append(c)
			print(str(a[0]) + ":" + str(a[1]) + "connected")


class Client:

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def __init__(self, address):
		self.sock.connect((address, 10000))
		# connect() argument is a tuple
		# First parameter of tuple is the address
		# Second parameter of tuple is the port

		iThread = threading.Thread(target=self.sendMsg)
		iThread.daemon = True
		iThread.start()
		# Create new thread to allow for sending data and receiving data

		while True:
			# Loop to continuosly send messages
			data = self.sock.recv(1024)
			if not data:
				break
			print(str(data, 'utf-8'))

	def sendMsg(self):
		# Allows client to send messages to server
		while True:
			# Continously ask for input
			self.sock.send(bytes(input(""), 'utf-8'))
			# Sends back the bytes of the input method in python
			# This bytes method also needs the encoding of the string (in this case
			# 	utf-8)
		

if len(sys.argv) > 1:
	# If there is more than 1 command line argument, we want to be the client
	client = Client(sys.argv[1])
	# Address for client is second command line argument
else :
	# Else we want to be the server
	server = Server()
	# Instantiate a server object
	server.run()