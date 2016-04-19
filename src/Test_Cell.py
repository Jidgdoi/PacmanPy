# -*- coding:utf-8 -*-

# Cyril Fournier
# 19/01/2016

import os
import unittest
from Cell import Cell

# ---------------------------
# --- Test Cell
# ---------------------------

class Test_Cell( unittest.TestCase ):
	
	def setUp(self):
		self.grid = Map()

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Test_Cell)
	unittest.TextTestRunner(verbosity=2).run(suite)
