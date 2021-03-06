# Thanks to kwatters
# https://github.com/MyRobotLab/pyrobotlab/blob/develop/home/kwatters/joystick_manticore.py

import math
import socket

#execfile('/home/scognito/dev/git/MRL/scripts/demo.py')
#execfile('C:\Users\scognito\git\scognito\MRL\scripts\demo.py')
#execfile('C:\dev\mrl\script\demo.py')

leftPort = "COM3"
#leftPort = "/dev/ttyACM0"

joystickIndex = 3; # check the index in the joy tab once running

# PIN
pinNeck = 12
pinRothead = 13
pinEyeX = 22
pinEyeY = 24
pinJaw = 26

# MIN / MAX FOR MAPPING
rotheadMin = 30  # left
rotheadMax = 160 # right
neckMin = 10
neckMax = 130
eyeXmin = 60  # left
eyeXmax = 120 # right
eyeYmin = 100
eyeYmax = 140
jawMin = 0
jawMax = 30

headVelocity = 45
joyThreshold = 0.5

# MAIN
i01 = Runtime.create("i01", "InMoov")

left = Runtime.createAndStart("i01.left", "Arduino")
left.connect(leftPort)
i01.startEar()

uberjoy = Runtime.createAndStart("joy", "Joystick")
uberjoy.setController(joystickIndex)
uberjoy.startPolling()

head = Runtime.create("i01.head","InMoovHead")

# MAPPING
head.neck.map(0, 180, neckMin, neckMax)
head.rothead.map(0, 180, rotheadMin, rotheadMax)
head.eyeX.map(0, 180, eyeXmin, eyeXmax)
head.eyeY.map(0, 180, eyeYmin, eyeYmax)
head.jaw.map(0, 180, jawMin, jawMax)

# SPEED
head.rothead.setVelocity(headVelocity)
head.neck.setVelocity(headVelocity)
head.eyeX.setVelocity(headVelocity)
head.eyeY.setVelocity(headVelocity)

# SET AUTODISABLE
head.rothead.enableAutoDisable(True);
head.neck.enableAutoDisable(True);
head.eyeX.enableAutoDisable(True);
head.eyeY.enableAutoDisable(True);

i01.startHead(leftPort)
i01.head.rothead.attach(left, pinRothead)
i01.head.neck.attach(left, pinNeck)
i01.head.eyeX.attach(left, pinEyeX)
i01.head.eyeY.attach(left, pinEyeY)
i01.head.jaw.attach(left, pinJaw)

python.subscribe("i01.ear","recognized") #FIX
ear = i01.ear
#ear.setLanguage("en-US")
ear.setLanguage("it-IT")
ear.startListening()

i01.startMouthControl(leftPort)
i01.mouthControl.setmouth(0, 180) # fa aprire e chiudere la bocca quando parla

def apriPortaLab():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
	s.connect(("therocks.it" , 80))
	s.sendall("GET /door/door-lab.php HTTP/1.1\r\nHost: therocks.it\r\n\r\n")
	print s.recv(4096)
	s.close

def apriPortaCed():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
	s.connect(("therocks.it" , 80))
	s.sendall("GET /door/door-ced.php HTTP/1.1\r\nHost: therocks.it\r\n\r\n")
	print s.recv(4096)
	s.close

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

def openMouth():
	i01.head.jaw.moveTo(180)

def closeMouth():
	i01.head.jaw.moveTo(0)
	
# used to disable servo buzzing
def disableServos():
	head.rothead.disable()
	head.neck.disable()
	head.eyeX.disable()
	head.eyeY.disable()
	
def sayTime():
	now = datetime.now()
	nowSay = "Sono le ore " + str(now.hour) + " e " + str(now.minute)
	i01.mouth.speak(nowSay)

def repeat(text):
	cutText = text[6:]
	i01.mouth.speak(cutText)
	
def onRecognized(text):
    # say rest
	if (text == u"rest" or text == u"relax" or text == u"riposo"):
		relax()
	elif( u"apri la porta del cell" in text or u"apri il cell" in text):
		mouth.speakBlocking("ok")
		apriPortaCed()
	elif( u"apri la porta" in text):
		mouth.speakBlocking("ok")
		apriPortaLab()
	elif( u"ciao" in text):
		mouth.speak("ciao")
	elif ( u"che ore sono" in text): # what time is it
		sayTime()
	elif ( u"porco dio" in text or "dio porco" in text or u"dioporco" in text  or u"porcodio" in text or u"dio cane" in text or u"diocane" in text):
		mouth.speak("non devi bestemmiare, porcoddio")
	#elif ( u"max" in text):
	#	mouth.speak('porcoddio')
	elif (text.startswith("ripeti")): # say
		repeat(text)
	elif (u"come ti chiami" in text): # what's your name
		#mouth.speak("pietro porcoddio")
		mouth.speak("mi chiamo Querti")
	elif (u"cosa fa dio" in text or u"che fa dio" in text):
		mouth.speak("abbaia, che cazzo deve fare")
	
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
	# L TRIGGER
	if ((data.id == '4' ) and float(data.value) == 1.0):
		openMouth()
	# R TRIGGER
	if ((data.id == '5' ) and float(data.value) == 1.0):
		closeMouth()

uberjoy.addInputListener(python)