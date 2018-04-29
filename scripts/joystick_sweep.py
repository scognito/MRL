import math
import time
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

i01.head.rothead.setSpeedControlOnUC(False)

def StickXListener(value):
  print "Stick X :" + str(value) + " Current pos: " + str(i01.head.rothead.pos)
  absValue = math.fabs(value)
  if (absValue < 0.175):
    print "Stop sweep"
    i01.head.rothead.stop()
    return
  absValue = absValue-0.01
  
  i01.head.rothead.setSpeed(absValue)
  delay = int((1-absValue) * 200)
  if (value > 0.0):
    print "Set Speed " + str(absValue)
    if (i01.head.rothead.isSweeping()):
      i01.head.rothead.setSweepDelay(delay)
    else:    
      i01.head.rothead.sweep(i01.head.rothead.pos, i01.head.rothead.max, delay, 1, True)
  else:
    if (i01.head.rothead.isSweeping()):
      i01.head.rothead.setSweepDelay(delay)
    else:
	i01.head.rothead.sweep(i01.head.rothead.min, i01.head.rothead.pos, delay, -1, True)

uberjoy.map("y", -1, 1, 1, -1)
uberjoy.map("ry", -1, 1, 1, -1)

def onJoystickInput(data):
	#print("id:" , data.id)
	if (data.id == "x"):
		#print "gigi"
		StickXListener(data.value)