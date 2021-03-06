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

class Elevator (Module):
	def __init__ (self, name):
		Module.__init__ (self, name)
		self.page ('internal data (READ-ONLY)')
		self.group ('state', True)
		self.reqUp      = Marker()
		self.reqDown    = Marker()
		self.goingUp    = Marker()
		self.goingDown  = Marker()
		self.idle       = Marker()
		self.shouldBreak= Marker()
		self.going      = Marker()
		self.breaking   = Marker()
		self.stopped    = Marker()
		self.atTopSpeed = Marker()
		self.stopTimer  = Timer()
		self.group ('physics', True)
		self.height     = Register(3.0)
		self.speed      = Register(0.0)
		self.acc        = Register(0.0)
		self.group ('button state', True)
		self.goto0 = Register()
		self.goto1 = Register()
		self.goto2 = Register()
		self.goto3 = Register()
		self.goto4 = Register()
		self.goto5 = Register()
		self.up1   = Register()
		self.up2   = Register()
		self.up3   = Register()
		self.up4   = Register()
		self.down1 = Register()
		self.down2 = Register()
		self.down3 = Register()
		self.down4 = Register()
		self.group ('misc', True)
		self.run = Runner ()

	def input (self, world):
		self.goto0.set(1,world.ctrl.goto0 or world.ctrl.up0)
		self.goto1.set(1,world.ctrl.goto1)
		self.goto2.set(1,world.ctrl.goto2)
		self.goto3.set(1,world.ctrl.goto3)
		self.goto4.set(1,world.ctrl.goto4)
		self.goto5.set(1,world.ctrl.goto5 or world.ctrl.down5)
		
		self.down1.set(1,world.ctrl.down1)
		self.down2.set(1,world.ctrl.down2)
		self.down3.set(1,world.ctrl.down3)
		self.down4.set(1,world.ctrl.down4)
		
		self.up1.set(  1,world.ctrl.up1)
		self.up2.set(  1,world.ctrl.up2)
		self.up3.set(  1,world.ctrl.up3)
		self.up4.set(  1,world.ctrl.up4)
		
		self.goto0.set(0, self.stopped and self.height<0.1 )
		self.goto1.set(0, self.stopped and self.height<1.1 and self.height>0.9 )
		self.goto2.set(0, self.stopped and self.height<2.1 and self.height>1.9 )
		self.goto3.set(0, self.stopped and self.height<3.1 and self.height>2.9 )
		self.goto4.set(0, self.stopped and self.height<4.1 and self.height>3.9 )
		self.goto5.set(0, self.stopped                     and self.height>4.9 )
		
		self.down1.set(0, self.goingDown and self.stopped and self.height<1.1 and self.height>0.9 )
		self.down2.set(0, self.goingDown and self.stopped and self.height<2.1 and self.height>1.9 )
		self.down3.set(0, self.goingDown and self.stopped and self.height<3.1 and self.height>2.9 )
		self.down4.set(0, self.goingDown and self.stopped and self.height<4.1 and self.height>3.9 )
		
		self.up1.set(  0, self.goingUp and self.stopped and self.height<1.1 and self.height>0.9 )
		self.up2.set(  0, self.goingUp and self.stopped and self.height<2.1 and self.height>1.9)
		self.up3.set(  0, self.goingUp and self.stopped and self.height<3.1 and self.height>2.9)
		self.up4.set(  0, self.goingUp and self.stopped and self.height<4.1 and self.height>3.9)

	def sweep (self):
		# if no button is pressed, it is idle
		self.idle.mark (not
		 (  self.goto0               
		 or self.goto1 or self.up1 or self.down1
		 or self.goto2 or self.up2 or self.down2
		 or self.goto3 or self.up3 or self.down3
		 or self.goto4 or self.up4 or self.down4
		 or self.goto5 ))
			
		# if the button is pressed above the current location of the elevator, the elevator is requested up
		self.reqUp.mark(
			(self.height < 4.9 and (self.goto5))
		 or (self.height < 3.9 and (self.goto4 or self.down4 or self.up4 ))
		 or (self.height < 2.9 and (self.goto3 or self.down3 or self.up3 ))
		 or (self.height < 1.9 and (self.goto2 or self.down2 or self.up2 ))
		 or (self.height < 0.9 and (self.goto1 or self.down1 or self.up1 )))
		 
		# if the button is pressed below the current location of the elevator, the elevator is requested down
		self.reqDown.mark(
			(self.height > 0.1 and (self.goto0))
		 or (self.height > 1.1 and (self.goto1 or self.down1 or self.up1 ))
		 or (self.height > 2.1 and (self.goto2 or self.down2 or self.up2 ))
		 or (self.height > 3.1 and (self.goto3 or self.down3 or self.up3 ))
		 or (self.height > 4.1 and (self.goto4 or self.down4 or self.up4 )))
		
		# if halfway to a floor where the button in the same direction is pressed, the elevator should stop
		self.shouldBreak.mark(
			(self.goingDown and self.height > 0 and self.height < 0.2 and  self.goto0)
		 or (self.goingDown and self.height > 1 and self.height < 1.2 and (self.goto1 or self.down1))
		 or (self.goingDown and self.height > 2 and self.height < 2.2 and (self.goto2 or self.down2))
		 or (self.goingDown and self.height > 3 and self.height < 3.2 and (self.goto3 or self.down3))
		 or (self.goingDown and self.height > 4 and self.height < 4.2 and (self.goto4 or self.down4))
		 or (self.goingUp   and self.height < 1 and self.height > 0.8 and (self.goto1 or self.up1))
		 or (self.goingUp   and self.height < 2 and self.height > 1.8 and (self.goto2 or self.up2))
		 or (self.goingUp   and self.height < 3 and self.height > 2.8 and (self.goto3 or self.up3))
		 or (self.goingUp   and self.height < 4 and self.height > 3.8 and (self.goto4 or self.up4))
		 or (self.goingUp   and self.height < 5 and self.height > 4.8 and  self.goto5))
		
		self.goingUp.mark((not self.goingDown) and self.reqUp)
		self.goingDown.mark((not self.goingUp) and self.reqDown)
		
		self.stopped.mark( (not self.going)   and self.speed > -0.001 and self.speed < 0.001)
		self.going.mark(   (not self.breaking)and (self.stopTimer > 10 and not self.idle))
		self.breaking.mark((not self.stopped) and self.shouldBreak)
		
		self.stopTimer.reset(self.breaking)
		
		self.atTopSpeed.mark(self.speed > 0.005 or self.speed < -0.005)
		# if at top speed
		self.acc.set( 0, self.going and self.atTopSpeed)
		# when accelerating up
		self.acc.set( 1, self.going and (not self.atTopSpeed) and self.goingUp)
		# when accelerating down
		self.acc.set(-1, self.going and (not self.atTopSpeed) and self.goingDown)
		# when decelerating
		self.acc.set(-self.speed*200, self.breaking)
		self.acc.set(0, self.stopped)
		self.speed.set(0, self.stopped)
		
		# simulate
		self.speed.set(self.speed+(self.acc*0.0001))
		self.height.set(self.height+self.speed)