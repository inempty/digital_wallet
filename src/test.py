#!/usr/bin/python

#import pandas as pd
import numpy as np

class usernet(object):
	""" a usernet consists of an array of users, and each user has an array 
	recording its relation with other users (friend or not). 
	"""
	def __init__(self, batchfilename, streamfilename):
		self.bfname = batchfilename
		self.sfname = streamfilename 

		self.userf = []
		self.num_edge = 0
		"""userf stores friendship of users"""
		self.read_batch()
		self.init_network()

	def read_batch(self):
		#df = pd.read_csv(self.bfname, sep = ',', names = ["time", "id1", "id2", "amount"])
		#print df['id1'].max()
		idmax = 0
		with open(self.bfname, 'r') as f:
			f.readline()
			line = f.readline()
			while(line):
				id1 = int(line.split()[2].rstrip(','))
				id2 = int(line.split()[3].rstrip(','))
				#print id1, id2
				line = f.readline()
				idtemp = max(id1, id2)
				idmax = max(idtemp, idmax)
			self.usernum = idmax + 1
			self.arraysize = self.usernum * (self.usernum - 1) / 2

			print "Totally ", self.usernum, " users are found."
			self.userf = np.zeros(self.arraysize, dtype = bool)

			f.seek(0, 0)
			f.readline()
			line = f.readline()
			while(line):
				id1 = int(line.split()[2].rstrip(','))
				id2 = int(line.split()[3].rstrip(','))
				ids = min(id1, id2)
				idb = max(id1, id2)

				ind = idb*(idb - 1) / 2 + ids
				if self.userf[ind] == False:
					self.num_edge += 1
				self.userf[ind] = True
				line = f.readline()

	def init_network(self):
		self.userf2 = np.zeros(self.arraysize, dtype = bool)
		self.userf3 = np.zeros(self.arraysize, dtype = bool)
		self.userf4 = np.zeros(self.arraysize, dtype = bool)

	def verify(self, feature, id1, id2):
		"""
		this function verifies a payment between id1 and id2.

		feature: int type, 1, 2 or 4; if it equals n, then only payment between nth degree friends is verified.
		id1: int type
		id2: int type
		rtype: bool
		"""
		
		ids = min(id1, id2)
		idb = max(id1, id2)
		ind = idb*(idb - 1) / 2 + ids

		if self.userf[ind] == True:
			return True

		if feature == 2:
			if self.userf2[ind] == True:
				return True
		if feature == 4:
			if self.userf3[ind] == True:
				return True

			if self.userf4[ind] == True:
				return True

		return False
	
	def update_network(self, id1, id2):
		"""
		id1: int type
		id2: int type
		rtype: none
		"""


net1 = usernet("../paymo_input/stream_payment.csv", "../paymo_input/stream_payment.csv")
print net1.num_edge

print net1.verify(1, 70, 100)
