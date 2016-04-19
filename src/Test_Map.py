# -*- coding:utf-8 -*-

# Cyril Fournier
# 13/01/2016

import os
import unittest
from Map import Map

<<<<<<< HEAD
# ---------------------------
# --- Test Map
# ---------------------------

class Test_Map( unittest.TestCase ):
	
	def setUp(self):
		self.grid = Map()
	
=======
class Test_Map( unittest.TestCase ):

	def setUp(self):
		self.grid = Map()

	# ---------------------------
	# --- Test Map
	# ---------------------------
>>>>>>> 3f97cd8ac787b2324de231df083dc8c8651628d6
	def test__createMap(self):
		print '\n', self.grid
		self.assertEqual('ok', 'ok')

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Test_Map)
	unittest.TextTestRunner(verbosity=2).run(suite)
