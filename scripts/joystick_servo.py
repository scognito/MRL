# Thanks to kwatters
# https://github.com/MyRobotLab/pyrobotlab/blob/develop/home/kwatters/joystick_manticore.py

import math

leftPort = "COM5"

joystickIndex = 2;

pinRothead = 13

rotheadMin = 30  # sx
rotheadMax = 160 # dx
rotheadVelocity = 45

joyThreshold = 0.5
joyGain = 100

i01 = Runtime.create("i01", "InMoov")

left = Runtime.createAndStart("i01.left", "Arduino")
left.connect(leftPort)

uberjoy = Runtime.createAndStart("joy", "Joystick")
uberjoy.setController(joystickIndex)
uberjoy.startPolling()

head = Runtime.create("i01.head","InMoovHead")
head.rothead.setVelocity(rotheadVelocity)
head.rothead.map(0, 180, rotheadMin, rotheadMax)

i01.startHead(leftPort)
i01.head.rothead.attach(left, pinRothead)

def StickXListener(value):

	global head
	
	absValue = math.fabs(value)

	# below the threshold, stop the servo where it is
	if (absValue < joyThreshold ):
		head.rothead.setVelocity(0)
		head.rothead.moveTo(head.rothead.pos)
	else:
		# set velocity to some amount based on the joystick position
		#velocity = absValue * joyGain
		#head.rothead.setVelocity(velocity)
		head.rothead.setVelocity(rotheadVelocity)
    		# set the direction of the movement
		if (value < 0):
			head.rothead.moveTo(head.rothead.min)
    		else:
			head.rothead.moveTo(head.rothead.max)
	
def onJoystickInput(data):
	if (data.id == "x"):
		StickXListener(data.value)

uberjoy.addInputListener(python)