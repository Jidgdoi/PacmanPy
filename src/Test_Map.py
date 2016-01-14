# -*- coding:utf-8 -*-

# Cyril Fournier
# 13/01/2016

import os
import unittest
from Map import Map

class Test_Map( unittest.TestCase ):

	def setUp(self):
		self.grid = Map()

	# ---------------------------
	# --- Test Map
	# ---------------------------
	def test__createMap(self):
		print '\n', self.grid
		self.assertEqual('ok', 'ok')

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Test_Map)
	unittest.TextTestRunner(verbosity=2).run(suite)
