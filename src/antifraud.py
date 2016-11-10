#!/usr/bin/python

import numpy as np
import time 
import sys
import os

class usernet(object):
	""" 
	a usernet consists of an array of users, 
	and each user has an array recording its direct 
	friends. (adjacency list rep. of graph)

	the class has two attribute:
	bfname: filename of batch_payment info.
	users: dict storing all users and their friends
	
	and three methods:
	read_batch: construct user network with batch file
	verify: verify a new transaction, and update the
	network when a new user appears.
	update: update network with new information
	"""
	def __init__(self, batchfilename):
		"""
		constructor

		batchfilename: filename for batch_payment info.
		"""
		self.bfname = batchfilename

		self.users = {}
		self.user_stat = {}
		""" 
		dict users stores each user as a key, 
		whose friends are stored as a set 
		"""
		self.read_batch()
		""" establish the network from batch file """

	def read_batch(self):
		"""
		read_batch function reads batch_payment from file,
		constructing the initial state of user network.
		"""
		with open(self.bfname, 'r') as f:
			f.readline()
			line = f.readline()
			while(line):
				id1 = line.split()[2].rstrip(',')
				id2 = line.split()[3].rstrip(',')
				amount = float(line.split()[4].rstrip(','))
				if id1 in self.users:
					self.users[id1].add(id2)

					#print self.user_stat[id1]
					#print id1, self.users[id1]
					no = self.user_stat[id1]["pay_num"] 
					avgo = self.user_stat[id1]["amount_avg"] 
					sigo = self.user_stat[id1]["amount_sig"] 

					self.user_stat[id1]["pay_num"] += 1
					self.user_stat[id1]["amount_avg"] *= float(no) / float(no + 1)
					self.user_stat[id1]["amount_avg"] += amount / float(no + 1)
					self.user_stat[id1]["amount_sig"] =\
							np.sqrt((sigo**2 * (no) + amount**2)/ float(no + 1))

				else:
					self.users[id1] = {id2}

					self.user_stat[id1] = {"pay_num": 1, "amount_avg": amount, "amount_sig": 0.0}
					#print id1, self.user_stat[id1], "+"

				if id2 in self.users:
					self.users[id2].add(id1)
					"""
					no = self.user_stat[id2].["pay_num"] 
					avgo = self.user_stat[id2].["amount_tot"] / float(no)
					sigo = self.user_stat[id2].["amount_sig"] 

					self.user_stat[id2].["pay_num"] += 1
					self.user_stat[id2].["amount_tot"] += amount
					self.user_stat[id2].["amount_sig"] =\
							np.sqrt((sigo**2 * (no - 1) + amount**2)/ float(no))
					"""
				else:
					self.users[id2] = {id1}
					
					self.user_stat[id2] = {"pay_num": 0, "amount_avg": 0, "amount_sig": 0.0}
					
				#print id1, id2
				line = f.readline()

	def verify(self, feature, id1, id2, amount):
		"""
		verify function verifies if users of id1 and id2 
		are friends up to nth degree, given n = feature.

		feature: int type, equals 1, 2, 3
		id1: string type, used as key in self.users
		id2: string type, used as key in self.users
		amount: float type amount of payment
		rtype: bool, int, int; first element shows if payment 
		is verified due to social network consideration; second
		shows up to which degree two users are "friends" (0 if 
		not even 4th friends); third shows additional information
		according to user's past information.
		"""

		if id1 not in self.users:
			return False, 0, 0 
		else:
			user1 = self.user_stat[id1]
			pay_num = user1["pay_num"]
			avg = user1["amount_avg"]
			sig = user1["amount_sig"]
			if amount > avg + 3*sig:
				ptype = 2
			else:
				ptype = 1

		if id2 not in self.users:
			return False, 0, ptype
		"""
		if id1 or id2 doesn't exist yet, exit directly
		"""

		result = (id2 in self.users[id1])

		if feature == 1 or result == True:
			return result, 1, ptype

		""" consider friend of friend"""

		result = bool(self.users[id1].intersection(self.users[id2])) 

		if feature == 2 or result == True:
			return result, 2, ptype

		""" consider up to 3rd degree friends"""

		for id1_friend in self.users[id1]:
			ff1 = self.users[id1_friend]
			result = bool(ff1.intersection(self.users[id2]))
			if result == True:
				return True, 3, ptype
		
		""" consider up to 4th degree friends"""

		ff1 = set()
		ff2 = set()
		for id1_friend in self.users[id1]:
			ff1 = self.users[id1_friend]
			for id2_friend in self.users[id2]:
				ff2 = self.users[id2_friend]
				result = bool(ff1.intersection(ff2))
				if result == True:
					return True, 4, ptype

		return result, 4, ptype

	def update(self, id1, id2, amount):
		"""
		id1: string type
		id2: string type
		"""
		if id1 not in self.users:
			self.users[id1] = {id2}

			self.user_stat[id1] = {"pay_num": 1, "amount_avg": amount, "amount_sig": 0.0}

		else:
			self.users[id1].add(id2)

			no = self.user_stat[id1]["pay_num"] 
			avgo = self.user_stat[id1]["amount_avg"] 
			sigo = self.user_stat[id1]["amount_sig"] 

			self.user_stat[id1]["pay_num"] += 1
			self.user_stat[id1]["amount_avg"] *= float(no) / float(no + 1)
			self.user_stat[id1]["amount_avg"] += amount / float(no + 1)
			self.user_stat[id1]["amount_sig"] =\
					np.sqrt((sigo**2 * (no) + amount**2)/ float(no + 1))


		if id2 not in self.users:
			self.users[id2] = {id1}

			self.user_stat[id2] = {"pay_num": 0, "amount_avg": 0.0, "amount_sig": 0.0}
		else:
			self.users[id2].add(id1)

"""
beginning of main program
"""

batch_file = sys.argv[1]
stream_file = sys.argv[2]
output = [sys.argv[3], sys.argv[4], sys.argv[5]]
sec_deg = int(sys.argv[6])

cwd = os.getcwd() + '/'


net1 = usernet(cwd + batch_file)

print "network is established."

with open(cwd + stream_file, 'r') as f:
	g = [open(cwd + output[u], 'w') for u in range(3)]

	f.readline()
	"""
	skip the first line
	"""
	line = f.readline()
	
	while line:

		linelist = line.split() 
		id1 = linelist[2].rstrip(',')
		id2 = linelist[3].rstrip(',')
		amount = float(linelist[4].rstrip(','))

		for u in range(3):
			result, degree, ptype = net1.verify(u + 1, id1, id2, amount)
			if result == True:
				status = 'trusted'
				if sec_deg > 1:
					if ptype == 2:
						status = 'trusted but suspicious'
			else:
				status = 'unverified'

			print >>g[u], status

		net1.update(id1, id2, amount)

		line = f.readline()

	for u in range(3):	
		g[u].close()

	print "Process exited."
