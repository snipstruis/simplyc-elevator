# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

from SimPyLC import *

class Ctrl (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		self.page ('elevator controlls')
		self.group ('outside buttons', True)
		self.up0   = Marker()
		self.down1 = Marker()
		self.up1   = Marker()
		self.down2 = Marker()
		self.up2   = Marker()
		self.down3 = Marker()
		self.up3   = Marker()
		self.down4 = Marker()
		self.up4   = Marker()
		self.down5 = Marker()
		self.group ('inside buttons', True)
		self.goto0 = Marker()
		self.goto1 = Marker()
		self.goto2 = Marker()
		self.goto3 = Marker()
		self.goto4 = Marker()
		self.goto5 = Marker()
		self.run = Runner ()
		
	def input (self, world):
		pass
	
	def sweep (self):
		pass
		