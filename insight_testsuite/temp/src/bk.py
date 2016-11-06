#!/usr/bin/python

import numpy as np
import time 
import sys
import os

class usernet(object):
	""" a usernet consists of an array of users, and each user has an array 
	recording its direct friends. (adjacency list rep. of graph)
	"""
	def __init__(self, batchfilename):
		self.bfname = batchfilename

		self.users = {}
		"""users stores each user as a key, whose friends are stored as a set"""
		self.read_batch()
		#self.init_network()

	def read_batch(self):
		#df = pd.read_csv(self.bfname, sep = ',', names = ["time", "id1", "id2", "amount"])
		#print df['id1'].max()
		idmax = 0
		with open(self.bfname, 'r') as f:
			f.readline()
			line = f.readline()
			while(line):
				id1 = line.split()[2].rstrip(',')
				id2 = line.split()[3].rstrip(',')
				if id1 in self.users:
					self.users[id1].add(id2)
				else:
					self.users[id1] = {id2}
				if id2 in self.users:
					self.users[id2].add(id1)
				else:
					self.users[id2] = {id1}
				#print id1, id2
				line = f.readline()

	def verify(self, feature, id1, id2):
		"""
		verify function verifies if users of id1 and id2 are friends up to nth degree, given
		n = feature.

		feature: int type, equals 1, 2, 3
		id1: string type, used as key in self.users
		id2: string type, used as key in self.users
		rtype: bool, int
		"""
		if id1 not in self.users:
			self.users[id1] = {id2}
			return False, 1
		if id2 not in self.users:
			self.users[id2] = {id1}
			return False, 1

		result = id2 in self.users[id1]

		if feature == 1 or result == True:
			return result, 1

		""" consider friend of friend"""

		result = bool(self.users[id1].intersection(self.users[id2])) 

		if feature == 2 or result == True:
			return result, 2

		""" consider up to 3rd degree friends"""

		for id1_friend in self.users[id1]:
			ff1 = self.users[id1_friend]
			result = bool(ff1.intersection(self.users[id2]))
			if result == True:
				return True, 3
		
		""" consider up to 4th degree friends"""

		ff1 = set()
		ff2 = set()
		for id1_friend in self.users[id1]:
			ff1 = ff1.union(self.users[id1_friend])

		for id2_friend in self.users[id2]:
			ff2 = ff2.union(self.users[id2_friend])

		result = bool(ff1.intersection(ff2))
		if result == True:
			return True, 4

		return result, 4

batch_file = sys.argv[1]
stream_file = sys.argv[2]
output = [sys.argv[3], sys.argv[4], sys.argv[5]]

cwd = os.getcwd() + '/'

#print cwd + batch_file, cwd + stream_file

#quit()


net1 = usernet(cwd + batch_file)

print "network is established."

with open(cwd + stream_file, 'r') as f:
	for u in range(3):
		g = open(cwd + output[u], 'w')

		f.seek(0, 0)
		"""
		file pointer of f is back to beginning
		"""
		f.readline()
		"""
		skip the first line
		"""
		line = f.readline()
	
		while line:

			id1 = line.split()[2].rstrip(',')
			id2 = line.split()[3].rstrip(',')

			result, degree = net1.verify(u + 1, id1, id2)

			if result == True:
				status = 'trusted'
			else:
				status = 'unverified'

			print >>g, status

			line = f.readline()

		g.close()
