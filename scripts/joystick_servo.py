# Thanks to kwatters
# https://github.com/MyRobotLab/pyrobotlab/blob/develop/home/kwatters/joystick_manticore.py

import math

#execfile('/home/scognito/dev/git/MRL/scripts/joystick_servo.py')

#leftPort = "COM5"
leftPort = "/dev/ttyACM0"

joystickIndex = 0; # check the index in the joy tab once running

# PIN
pinNeck = 12
pinRothead = 13
pinEyeX = 22
pinEyeY = 24

# MIN / MAX FOR MAPPING
rotheadMin = 30  # left
rotheadMax = 160 # right
neckMin = 10
neckMax = 130
eyeXmin = 60  # left
eyeXmax = 120 # right
eyeYmin = 100
eyeYmax = 140

headVelocity = 45
joyThreshold = 0.5

# MAIN
i01 = Runtime.create("i01", "InMoov")

left = Runtime.createAndStart("i01.left", "Arduino")
left.connect(leftPort)

uberjoy = Runtime.createAndStart("joy", "Joystick")
uberjoy.setController(joystickIndex)
uberjoy.startPolling()

head = Runtime.create("i01.head","InMoovHead")

# MAPPING
head.neck.map(0, 180, neckMin, neckMax)
head.rothead.map(0, 180, rotheadMin, rotheadMax)
head.eyeX.map(0, 180, eyeXmin, eyeXmax)
head.eyeY.map(0, 180, eyeYmin, eyeYmax)

# SPEED
head.rothead.setVelocity(headVelocity)
head.neck.setVelocity(headVelocity)
head.eyeX.setVelocity(headVelocity)
head.eyeY.setVelocity(headVelocity)

# SET AUTODISABLE
#head.rothead.setAutoDisable(True);
#head.neck.setAutoDisable(True);
#head.eyeX.setAutoDisable(True);
#head.eyeY.setAutoDisable(True);

i01.startHead(leftPort)
i01.head.rothead.attach(left, pinRothead)
i01.head.neck.attach(left, pinNeck)
i01.head.eyeX.attach(left, pinEyeX)
i01.head.eyeY.attach(left, pinEyeY)

def leftStickXYListener(axis, value):

	global head
	
	absValue = math.fabs(value)

	# below the threshold, stop the servo where it is
	if (absValue < joyThreshold):
		if(axis == "x"):
			if(head.rothead.getVelocity() > 0):
				#print "A: " + str(head.rothead.getVelocity())
				head.rothead.setVelocity(0)
				head.rothead.moveTo(head.rothead.pos)
				#head.rothead.disable()
		else:
			if(head.neck.getVelocity() > 0):
				#print "B: " + str(head.neck.getVelocity())
				head.neck.setVelocity(0)
				head.neck.moveTo(head.neck.pos)
				#head.neck.disable()
	else:
		# set velocity to some amount based on the joystick position
		if(axis == "x"):
			#print "C *****"
			head.rothead.setVelocity(headVelocity)
		else:
			#print "D ****"
			head.neck.setVelocity(headVelocity)
			
			# set the direction of the movement
		if(value < 0):
			if(axis == "x"):
				head.rothead.moveTo(head.rothead.min)
			else:
				head.neck.moveTo(head.neck.max)
		else:
			if(axis == "x"):
				head.rothead.moveTo(head.rothead.max)
			else:
				head.neck.moveTo(head.neck.min)

def rightStickXYListener(axis, value):

	global head
	
	absValue = math.fabs(value)

	# below the threshold, stop the servo where it is
	if (absValue < joyThreshold):
		if(axis == "x"):
			if(head.eyeX.getVelocity() > 0):
				head.eyeX.setVelocity(0)
				head.eyeX.moveTo(head.eyeX.pos)
		else:
			if(head.eyeY.getVelocity() > 0):
				head.eyeY.setVelocity(0)
				head.eyeY.moveTo(head.eyeY.pos)
	else:
		# set velocity to some amount based on the joystick position
		if(axis == "x"):
			head.eyeX.setVelocity(headVelocity)
		else:
			head.eyeY.setVelocity(headVelocity)
			
		# set the direction of the movement
		if (value > 0):
			if(axis == "x"):
				head.eyeX.moveTo(head.eyeX.min)
			else:
				head.eyeY.moveTo(head.eyeY.max)
		else:
			if(axis == "x"):
				head.eyeX.moveTo(head.eyeX.max)
			else:
				head.eyeY.moveTo(head.eyeY.min)

# used to disable servo buzzing
def disableServos():
	head.rothead.disable()
	head.neck.disable()
	head.eyeX.disable()
	head.eyeY.disable()
	
def onJoystickInput(data):

	# left stick X axis
	if (data.id == "x"):
		leftStickXYListener("x", data.value)
	# left stick Y axis	
	if (data.id == "y"):
		leftStickXYListener("y", data.value)
	# right stick X axis
	if (data.id == "rx"):
		rightStickXYListener("x", data.value)
	# right stick Y axis
	if (data.id == "ry"):
		rightStickXYListener("y", data.value)

	# CIRCLE button
	if ((data.id == '1' or data.id == 'A') and float(data.value) == 1.0):
		disableServos()
		
uberjoy.addInputListener(python)