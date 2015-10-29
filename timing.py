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

class Timing (Chart):
	def __init__ (self, name):
		Chart.__init__ (self, name)
		
	def define (self, world):
		self.channel (world.elevator.acc,      red, -1, 1, 50)
		self.channel (world.elevator.speed,    yellow, -0.01, 0.01, 50)
		self.channel (world.elevator.height,   white, 0, 5, 200)
		self.channel (world.elevator.shouldBreak,green)
		self.channel (world.elevator.going,      blue)
		self.channel (world.elevator.breaking,   blue)
		self.channel (world.elevator.stopped,    blue)
		self.channel (world.elevator.stopTimer,  green, 0, 10, 60)
		