import math
# API JAVA https://github.com/MyRobotLab/myrobotlab/blob/05ef7ca86b67623593e2e94089202b63f676aa02/src/org/myrobotlab/service/Joystick.java
joystickIndex = 2;

pinRothead = 13

rotheadMin = 30  # sx
rotheadMax = 160 # dx

rotheadRest = 95
rotheadVelocity = 45

leftPort = "COM5"

i01 = Runtime.create("i01", "InMoov")

left = Runtime.createAndStart("i01.left", "Arduino")
left.connect(leftPort)

uberjoy = Runtime.createAndStart("joy", "Joystick")

uberjoy.setController(joystickIndex)
uberjoy.addInputListener(python)
#uberjoy.startPolling()

head = Runtime.create("i01.head","InMoovHead")
head.rothead.setVelocity(rotheadVelocity)
head.rothead.map(0, 180, rotheadMin, rotheadMax)

head.rothead.setSpeedControlOnUC(False)

i01.startHead(leftPort)
i01.head.rothead.attach(left, pinRothead)

#head.rothead.moveTo(30)
#head.rothead.sweep(head.rothead.pos, head.rothead.max, 50, 1, True)

print ("starting joypad")

def StickXListener(value):

	#print "Stick X :" + str(value) + " Current pos: " + str(head.rothead.pos)
	
	absValue = math.fabs(value)
  
	if (absValue < 0.250):
		if(head.rothead.isSweeping()):
			print "Stop sweep"
			head.rothead.stop()
			return
  
  	absValue = absValue - 0.01
	#print "Set Speed " + str(absValue)
	head.rothead.setSpeed(absValue)
	delay = int((1-absValue) * 200)
  
	if (value >= 0.250):

		if (head.rothead.pos == head.rothead.max):
			print "DESTRA MAX RAGGIUNTA"
			head.rothead.stop
	
		print "DESTRA"
		if (head.rothead.isSweeping()):
			head.rothead.setSweepDelay(delay)
			g = 0
		else:
			#sweep(double min, double max, int delay, double step, boolean oneWay)
			head.rothead.sweep(head.rothead.pos, 180, delay, 1, True)
	if (value <= -0.250):
		print "SINISTRA"
		if (head.rothead.isSweeping()):
			q = 0
			head.rothead.setSweepDelay(delay)
		else:
			head.rothead.sweep(0, head.rothead.pos, delay, -1, True)

#uberjoy.addListener("publishX", "python", "StickXListener")

def onJoystickInput(data):
	#print("id:" , data.id)
	if (data.id == "x"):
		#print "gigi"
		StickXListener(data.value)
	if (data.id == '0' and float(data.value) == 1.0):
		print ("Values min: ", head.rothead.min)
		print ("Values max: ", head.rothead.max)
		print ("Values pos: ", head.rothead.pos)