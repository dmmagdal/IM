# Diego Magdaleno
# Tutorial on how to create a simple python server
# Tutorial on how to create a simple python chat server
# Tutorial on how to create a simple python p2p chat server

import socket
import threading
import sys
import time
from random import randint

class Server:

	connections = []
	# An empty list of connections
	peers = []
	# A list of peers

	def __init__(self):
		# Simple constructor
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# AF_INET means using ipv4 (vs ipv6)
		# SOCK_STREAM means using a TCP connection
		# To have a UTP connection, replace SOCK_STREAM with SOCK_DGRAM
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Allows us to reuse a socket
		sock.bind(("0.0.0.0", 10000))
		# Bind socket to an address and port
		# Parentheses is python toggle
		# First parameter in parenthesis is address
		# Second parameter in parnethesis is port
		# "0.0.0.0" was chosen to make it available to any ip address 
		# 	available on the server
		# Port 10000 was just chosen arbitrarily

		sock.listen(1)
		# Listen
		# Pass in the number of connections we want to allow

		print("Server running ...")

		while True:
			# Create loop to handle connections
			c, a = sock.accept()
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
			self.peers.append(a[0])
			self.sendPeers()
			print(str(a[0]) + ":" + str(a[1]) + "connected")

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
				self.peers.remove(a[0])
				c.close()
				# Close connection
				self.sendPeers()
				# update the peers
				break
				# Allows to break out of loop

	def  sendPeers(self):
		# update the list of peers connected to the server
		p = ""
		for peer in self.peers:
			p = p + peer + ","
		for connection in self.connections:
			# Send list of peers
			connection.send(b'\x11' + bytes(p, 'utf-8'))
			# The \x11 is sending the byte at hte start of the string 
			# 	to differenciate between the list of peers and a message


class Client:

	def __init__(self, address):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.connect((address, 10000))
		# connect() argument is a tuple
		# First parameter of tuple is the address
		# Second parameter of tuple is the port

		iThread = threading.Thread(target = self.sendMsg, args = (sock, ))
		iThread.daemon = True
		iThread.start()
		# Create new thread to allow for sending data and receiving data

		while True:
			# Loop to continuosly send messages
			data = sock.recv(1024)
			if not data:
				break
			if data[0] == b'\x11':
				# If the first byte of data is \x11
				self.updatePeers(data[1:])
				# Update our peers
				# We've received the list of peers
			else:
				print(str(data, 'utf-8'))

	def sendMsg(self, sock):
		# Allows client to send messages to server
		while True:
			# Continously ask for input
			sock.send(bytes(input(""), 'utf-8'))
			# Sends back the bytes of the input method in python
			# This bytes method also needs the encoding of the string (in this case
			# 	utf-8)

	def updatePeers(self, peerData):
		p2p.peers = str(peerData, 'utf-8').spit(",")[:-1]

		
class p2p:
	peers = []
	# Peers list can have a default set of peers
	# ie peers = ['127.0.0.1'] "us"


while True:
	try:
		print("Trying to connect ...")
		time.sleep(randint(1, 5))
		# Sleep for a random amount of time (1 or 5 seconds)
		for peer in p2p.peers:
			try:
				client = Client(peer)
				# Try to create new client object from peers
			except  KeyboardInterrupt:
				# Another exception to allow the user to press Ctrl-C
				sys.exit(0)
			except:
				# If there is any other kind of exception, ignore it
				pass
			if randint(1, 20) == 1:
				# There is a 1 in 20 chance that the number will be 1
				# Which means that on average, 1 in 20 clients will try to become
				# 	the server
				# This gets around the problem of every client trying to become 
				# 	the server 
				try:
					# If we try to connect to any of the peers but with no success
					server = Server()
					# We become the server
				except  KeyboardInterrupt:
					sys.exit(0)
				except:
					# If that doesn't work, we're going to print
					print("Couldn't start server ...")
	except KeyboardInterrupt:
		# If you press Ctrl-C on the keyboard, we just exit the program
		sys.exit(0)