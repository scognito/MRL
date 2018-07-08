import math

#execfile('/home/scognito/dev/git/MRL/scripts/joy_voice.py')

leftPort = "/dev/ttyACM0"

# PIN
pinEyeX = 22
pinEyeY = 24
pinNeck = 12
pinRothead = 13
pinJaw = 26

# RANGE MIN MAX
eyeXmin = 60  # left
eyeXmax = 120 # right
eyeXrest = 90

eyeYmin = 100
eyeYmax = 140
eyeYrest = 115

neckMin = 10
neckMax = 130
neckRest = 90

jawMin = 0
jawMax = 30

rotheadMin = 30  # sx
rotheadMax = 160 # dx
rotheadRest = 95

# VELOCITY
headVelocity = 45
eyesVelocity = 45

# JOYSTICK START
joystickIndex = 0; # check the index in the joy tab once running
joyThreshold = 0.5
joyCheck = False

uberjoy = Runtime.createAndStart("joy", "Joystick")
uberjoy.setController(joystickIndex)
uberjoy.startPolling()

# JOYSTICK END

voice="cmu-bdl-hsmm"
#voice="istc-lucia-hsmm"

mouth = Runtime.createAndStart("i01.mouth", "MarySpeech")
#mouth = Runtime.createAndStart("i01.mouth", "NaturalReaderSpeech")
mouth.setVoice(voice)

i01 = Runtime.create("i01", "InMoov")

left = Runtime.createAndStart("i01.left", "Arduino")
left.connect(leftPort)
i01.startEar()

WebGui = Runtime.create("WebGui","WebGui")
WebGui.autoStartBrowser(False)
WebGui.startService()

head = Runtime.create("i01.head","InMoovHead")

# MAPPING
head.eyeX.map(0, 180, eyeXmin, eyeXmax)
head.eyeY.map(0, 180, eyeYmin, eyeYmax)
head.neck.map(0, 180, neckMin, neckMax)
head.jaw.map(0, 180, jawMin, jawMax)
head.rothead.map(0, 180, rotheadMin, rotheadMax)

# SPEED
head.rothead.setVelocity(headVelocity)
head.neck.setVelocity(headVelocity)
head.eyeX.setVelocity(eyesVelocity)
head.eyeY.setVelocity(eyesVelocity)

# REST
head.eyeX.setRest(eyeXrest)
head.eyeY.setRest(eyeYrest)
head.rothead.setRest(rotheadRest);

i01.startHead(leftPort)
i01.head.eyeX.attach(left, pinEyeX)
i01.head.eyeY.attach(left, pinEyeY)
i01.head.rothead.attach(left, pinRothead)
i01.head.neck.attach(left, pinNeck)
i01.head.jaw.attach(left, pinJaw)

i01.startMouthControl(leftPort)
i01.mouthControl.setmouth(0, 180)

head.setAutoDisable(True)
python.subscribe("i01.ear","recognized") #FIX
ear = i01.ear
#ear.setLanguage("en-US")
ear.setLanguage("it-IT")
ear.startListening()

print ("rothead min: " + str(head.rothead.min));
print ("rothead max: " + str(head.rothead.max));

def relax():
	i01.head.eyeX.moveTo(eyeXrest)
	i01.head.eyeY.moveTo(eyeYrest)
	i01.head.neck.moveTo(neckRest)
	i01.head.rothead.moveTo(rotheadRest)
	i01.head.jaw.moveTo(0)

relax()

def onRecognized(text):
    # say rest
	if (text == u"rest" or text == u"relax" or text == u"riposo"):
		relax()
	elif(text == u"hello" or text == u"ciao"):
		mouth.speak("hello")
    # look right
	elif (text == u"look right" or text == u"guarda a destra"):
		lookRight()
    # look left
	elif (text == u"look left" or text == u"guarda a sinistra"):
		lookLeft()
    # look up
	elif (text == u"look up" or text == u"guarda in alto"):
		lookUp()
    # look down
	elif (text == u"look down" or text == u"guarda in basso"):
		lookDown()
    # open mouth
	elif (text == u"open mouth" or text == u"apri la bocca"):
		openMouth()
    # close mouth
	elif (text == u"close mouth" or text == u"chiudi la bocca"):
		closeMouth()
    # turn head right
	elif (text == u"face right" or text == u"gira a destra"):
		rotateRight()
    # turn head left    
	elif (text == u"face left" or text == u"gira a sinistra"):
		rotateLeft()
    # turn head up
	elif (text == u"face up" or text == u"face app" or text == u"alza la testa" ):
		headUp()
    # turn head down
	elif (text == u"face down" or text == u"abbassa la testa"):
		headDown()

def rotateRight():
	i01.head.rothead.moveTo(0)
  
def rotateLeft():
	i01.head.rothead.moveTo(180)

def openMouth():
	i01.head.jaw.moveTo(180)

def closeMouth():
	i01.head.jaw.moveTo(0)

def lookUp():
	i01.head.eyeX.rest()
	i01.head.eyeY.moveTo(0)
	
def lookDown():
	i01.head.eyeX.rest()
	i01.head.eyeY.moveTo(180)

def lookLeft():
	i01.head.eyeY.rest()
	i01.head.eyeX.moveTo(0)

def lookRight():
	i01.head.eyeY.rest()
	i01.head.eyeX.moveTo(180)
	
def headDown():
	i01.head.neck.moveTo(0)
	
def headUp():
	i01.head.neck.moveTo(180)

# used to disable servo buzzing
def disableServos():
	head.rothead.disable()
	head.neck.disable()
	head.eyeX.disable()
	head.eyeY.disable()

# JOYSTICK START
def leftStickXYListener(axis, value):

	global head, joyCheck
	
	absValue = math.fabs(value)

	# below the threshold, stop the servo where it is
	if (absValue < joyThreshold):
		if(joyCheck == True):
			print "entro con axis: " + axis
			joyCheck = False
			if(axis == "x"):
				if(head.rothead.getVelocity() > 0):
					print "A: " + str(head.rothead.getVelocity())
					head.rothead.setVelocity(0)
					head.rothead.moveTo(head.rothead.pos)
				#head.rothead.disable()
					#head.rothead.moveTo(head.rothead.pos)
					#head.rothead.disable()
			else:
				if(head.neck.getVelocity() > 0):
					print "B: " + str(head.neck.getVelocity())
					head.neck.setVelocity(0)
					head.neck.moveTo(head.neck.pos)
					#head.neck.disable()
	else:
		joyCheck = True
		# set velocity to some amount based on the joystick position
		print "moving on axis: " + axis
		if(axis == "x"):
			head.rothead.setVelocity(headVelocity)
		else:
			head.neck.setVelocity(headVelocity)
			
		# set the direction of the m\ovement
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

	global head, joyCheck
	
	absValue = math.fabs(value)

	# below the threshold, stop the servo where it is
	if (absValue < joyThreshold):
		if(joyCheck == True):
			joyCheck = False

			if(axis == "x"):
				if(head.eyeX.getVelocity() > 0):
					head.eyeX.setVelocity(0)
					head.eyeX.moveTo(head.eyeX.pos)
			else:
				if(head.eyeY.getVelocity() > 0):
					head.eyeY.setVelocity(0)
					head.eyeY.moveTo(head.eyeY.pos)
	else:
		joyCheck = True
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
	if ((data.id == '1' or data.id == 'B') and float(data.value) == 1.0):
		disableServos()
	# CROSS button
	if ((data.id == '2' or data.id == 'A') and float(data.value) == 1.0):
		head.rothead.setVelocity(0)
		head.rothead.moveTo(head.rothead.pos)
		
uberjoy.addInputListener(python)
# JOYSTICK END