import sys
from time import sleep, time
from random import choice, random, randint
from string import letters

from PodSix.Concurrent import Concurrent

from PodSixNet.Connection import connection, ConnectionListener

class NetMonitor(ConnectionListener, Concurrent):
	def __init__(self, parent):
		self.parent = parent
		Concurrent.__init__(self)
		# do we have a current connection with the server?
		self.serverconnection = 0
		self.playerID = None
		self.queued = {}
		self.lastConnect = 0
		# randomly have an ID already (clients which have connected before)
		#if randint(0, 1) and len(self.demo_ids):
		#	self.playerID = self.demo_ids.pop()
		#	self.Send({"action": "playerid", "id": self.playerID})
		#else:
			# request a new UUID secret player ID to begin with
	
	def Connect(self):
		self.lastConnect = time()
		connection.DoConnect((self.parent.serverhost, 31415))
		packet = {"action": "playerid"}
		if self.playerID:
			packet.update({"id": self.playerID})
		self.Send(packet)
	
	def SendWithID(self, data):
		# send a data packet with this player's ID included, unless they don't have one
		# which should disconnect us from the server
		if self.playerID:
			data.update({"id": self.playerID})
		# send if we are connected
		if self.serverconnection == 1:
			self.Send(data)
			return True
		else:
			# queue up the unsent action data
			self.queued[data['action']] = data
			return False
	
	def Disconnect(self):
		if self.serverconnection == 1:
			connection.Close()
		self.serverconnection = 2
	
	def Pump(self):
		connection.Pump()
		ConnectionListener.Pump(self)
		Concurrent.Pump(self)
		# try and reconnect every 30 seconds
		if self.serverconnection != 1 and time() > self.lastConnect + 30:
			self.Connect()
	
	def ResendQueue(self):
		for a in self.queued:
			data = self.queued[a]
			data.update({"id": self.playerID})
			self.Send(self.queued[a])
			if "debug" in sys.argv:
				print "NetMonitor QUEUED:", self.queued[a]
		self.queued = {}
	
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	def Network(self, data):
		if "debug" in sys.argv:
			print "NetMonitor Received:", data
	
	def Network_playerid(self, data):
		# got my player ID, now send a new level i want to be on
		self.playerID = data['id']
		#self.SendWithID({"action": "setlevel", "level": choice(self.levels)})
		self.ResendQueue()
	
	def Network_player_entering(self, data):
		if "debug" in sys.argv:
			print "NetMonitor", self.playerID, "Saw player with ID %d" % data['id']
	
	# built in stuff
	
	def Network_connected(self, data):
		self.serverconnection = 1
		# check if we have actions queued
		if self.playerID:
			self.ResendQueue()
	
	def Network_error(self, data):
		self.serverconnection = 2
		connection.Close()
	
	def Network_disconnected(self, data):
		self.serverconnection = 2

