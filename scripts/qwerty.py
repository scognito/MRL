import time, math
from random import randint
from datetime import datetime
from threading import Thread

joystickIndex = 2;

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

VELOCITY_NORMAL = 3
VELOCITY_MAX = 1
velocity_pad = VELOCITY_NORMAL

eyeXvelocity = 100 # -1 full speed
eyeYvelocity = 100
neckVelocity = 45
rotheadVelocity = 45

leftPort = "COM5"
#voice="cmu-bdl-hsmm"
#voice="istc-lucia-hsmm"
voice="Italian_Francesco"

#music
maxSongs = 4
curSong = 0

#mouth = Runtime.createAndStart("i01.mouth", "MarySpeech")
mouth = Runtime.createAndStart("i01.mouth", "NaturalReaderSpeech")
mouth.setVoice(voice)
i01 = Runtime.create("i01", "InMoov")

left = Runtime.createAndStart("i01.left", "Arduino")
left.connect(leftPort)
i01.startEar()

WebGui = Runtime.create("WebGui","WebGui")
WebGui.autoStartBrowser(False)
WebGui.startService()
#WebGui.startBrowser("http://localhost:8888/#/service/i01.ear")

# JOYSTICK START
uberjoy = Runtime.createAndStart("joy", "Joystick")
uberjoy.setController(joystickIndex)
uberjoy.startPolling()

joyThreshold = 0.2
joyGain = 100

# JOYSTICK END

head = Runtime.create("i01.head","InMoovHead")

def normalVelocity():
	velocity_pad = VELOCITY_NORMAL
	head.eyeX.setVelocity(eyeXvelocity)
	head.eyeY.setVelocity(eyeYvelocity)
	head.neck.setVelocity(neckVelocity)
	head.rothead.setVelocity(rotheadVelocity)

normalVelocity()

# MAPPING
head.eyeX.map(0, 180, eyeXmin, eyeXmax)
head.eyeY.map(0, 180, eyeYmin, eyeYmax)
head.neck.map(0, 180, neckMin, neckMax)
head.jaw.map(0, 180, jawMin, jawMax)
head.rothead.map(0, 180, rotheadMin, rotheadMax)

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
i01.mouthControl.setmouth(0, 180) # fa aprire e chiudere la bocca quando parla

#i01.head.jaw.setMinMax(jawMin, jawMax)

#i01.startEyesTracking(leftPort, pinEyeX, pinEyeY)
i01.startHeadTracking(leftPort, pinRothead, pinNeck)
#i01.eyesTracking.pid.setPID("eyeX", 12.0,1.0,0.1)
#i01.eyesTracking.pid.setPID("eyeY", 12.0,1.0,0.1)
i01.headTracking.pid.setPID("rothead", 10.0, 1.0, 0.1)
i01.headTracking.pid.setPID("neck", 10.0, 1.0, 0.1)
# LKI WORKING
#i01.headTracking.pid.setPID("rothead", 5.0, 1.0, 0.1)
#i01.headTracking.pid.setPID("neck", 5.0, 1.0, 0.1)

head.setAutoDisable(True)
i01.head.rothead.setAutoDisable(True);
i01.head.neck.setAutoDisable(True);

python.subscribe("i01.ear","recognized") #FIX
ear = i01.ear
ear.setLanguage("it-IT")
ear.startListening()

def stopTracking():
	normalVelocity()
	i01.headTracking.stopTracking()
	#i01.eyesTracking.stopTracking()

def relax():
	normalVelocity()
	i01.mouth.audioFile.silence()
	stopTracking()
	#i01.mouth.speak("va bene.")
	i01.head.eyeX.moveTo(eyeXrest)
	i01.head.eyeY.moveTo(eyeYrest)
	i01.head.neck.moveTo(neckRest)
	i01.head.rothead.moveTo(rotheadRest)
	i01.head.jaw.moveTo(0)
	#i01.headTracking.stopTracking()
	#i01.head.rothead.moveTo(rotheadRest)
	
relax()

# FIX
# ear.setLanguage("it-IT")
# ear.addCommand("riposo", "python", "relax")
# ear.addCommand("guarda a destra", "python", "lookRight")
# ear.addCommand("guarda a sinistra", "python", "lookLeft")
# ear.addCommand("guarda in alto", "python", "lookUp")
# ear.addCommand("guarda in basso", "python", "lookDown")
# ear.addCommand("apri la bocca", "python", "openMouth")
# ear.addCommand("chiudi la bocca", "python", "closeMouth")
# ear.addCommand("gira a destra", "python", "rotateRight")
# ear.addCommand("gira a sinistra", "python", "rotateLeft")
# ear.addCommand("alza la testa", "python", "headUp")
# ear.addCommand("abbassa la testa", "python", "headDown")
# ear.addCommand("suca", "python", "suca")
# ear.addCommand("traccia", "python", "startLKTracking")
# ear.addCommand("stop traccia", "python", "stopTracking");
# ear.addCommand("musica", "python", "startMp3")
# ear.addCommand("silenzio", "python", "stopMp3")

def onRecognized(text):
	if (text == u"riposo" or text == u"riposa"):
		relax()
	elif (text == u"guarda a destra"):
		lookRight()
	elif (text == u"guarda a sinistra"):
		lookLeft()
	elif (text == u"guarda in alto" or text == u"alza lo sguardo"):
		lookUp()
	elif (text == u"guarda in basso" or text == u"abbassa lo sguardo"):
		lookDown()
	elif (text == u"apri la bocca"):
		openMouth()
	elif (text == u"chiudi la bocca"):
		closeMouth()
	elif (text == u"gira a destra" or text == u"gira la testa a destra"):
		rotateRight()
	elif (text == u"gira a sinistra" or text == u"gira la testa a sinistra"):
		rotateLeft()
	elif (text == u"alza la testa"):
		headUp()
	elif (text == u"abbassa la testa"):
		headDown()
	elif (text == u"suca"):
		suca()
	elif (text == u"traccia"):
		#startHumanTracking()
		startLKTracking()
	elif (text == u"non tracciare"):
		stopTracking()
	elif (text == u"musica"):
		startMp3()
	elif (text == u"silenzio"):
		stopMp3()
	elif (text == u"che ore sono"):
		sayTime()
	elif (text.startswith("ripeti")):
		repeat(text)
	elif (text == u"come ti chiami"):
		mouth.speak("mi chiamo Querti")
	elif (text == u"prova"):
		test123()	

def maxVelocity():
	velocity_pad = VELOCITY_MAX
	head.eyeX.setVelocity(-1)
	head.eyeY.setVelocity(-1)
	head.neck.setVelocity(-1)
	head.rothead.setVelocity(-1)

def test123():
	 if (i01.RobotIsOpenCvCapturing()):
	 	mouth.speak("smetto di tracciare")
		i01.opencv.removeFilter("Gray")
		i01.opencv.removeFilter("PyramidDown")
		i01.opencv.removeFilter("FaceRecognizer")
		i01.startHeadTracking(leftPort, pinRothead, pinNeck)
		sleep(1)
		i01.headTracking.faceDetect()
	    	#i01.eyesTracking.faceDetect()
		#i01.setHeadVelocity(80, -1)
	 else:
	 	mouth.speak("inizio a tracciare")
	 	i01.startHeadTracking(leftPort, pinRothead, pinNeck)
    		sleep(1)
    		i01.headTracking.faceDetect()
    		i01.setHeadVelocity(80, -1)
    		sleep(1)
		#fullspeed()
	 	
def startLKTracking():
	maxVelocity()
	i01.headTracking.startLKTracking()

def startHumanTracking():
	i01.headTracking.faceDetect()
	
def startMp3():
	i01.mouth.audioFile.silence()
	time.sleep(1)

	global curSong, maxSongs

	if(curSong == maxSongs - 1):
		curSong = 0
	
	#curSong = randint(0, 3)
	if (curSong == 0):
		mouth.speakBlocking("Riproduco i blinc 182")
		i01.mouth.audioFile.playFile("C:/dev/mrl/scripts/mp3/blink.mp3", False)
	elif (curSong == 1):
		mouth.speakBlocking("Riproduco emi uainaus")
		i01.mouth.audioFile.playFile("C:/dev/mrl/scripts/mp3/amy.mp3", False)
	elif (curSong == 2):
		mouth.speakBlocking("Riproduco i ramones")
		i01.mouth.audioFile.playFile("C:/dev/mrl/scripts/mp3/ramones.mp3", False)
	elif (curSong == 3):
		mouth.speakBlocking("Riproduco i dair streits")
		i01.mouth.audioFile.playFile("C:/dev/mrl/scripts/mp3/sultan.mp3", False)

	curSong = curSong+1
#	audioFile = Runtime.createAndStart("af1", "AudioFile");
#	audioFile.playFile("my.mp3" False); # autostart

def stopMp3():
	i01.mouth.audioFile.silence()

def rotateRight():
	normalVelocity()
	i01.head.rothead.moveTo(0)
  
def rotateLeft():
	normalVelocity()
	i01.head.rothead.moveTo(180)

def suca():
	i01.mouth.speak("vafanculo coglione")
	
def openMouth():
	i01.head.jaw.moveTo(180)

def closeMouth():
	i01.head.jaw.moveTo(0)

def lookUp():
	normalVelocity()
	i01.head.eyeX.rest()
	i01.head.eyeY.moveTo(0)
	
def lookDown():
	normalVelocity()
	i01.head.eyeX.rest()
	i01.head.eyeY.moveTo(180)

def lookLeft():
	normalVelocity()
	i01.head.eyeY.rest()
	i01.head.eyeX.moveTo(0)

def lookRight():
	normalVelocity()
	i01.head.eyeY.rest()
	i01.head.eyeX.moveTo(180)
	
def headDown():
	normalVelocity()
	i01.head.neck.moveTo(0)
	
def headUp():
	normalVelocity()
	i01.head.neck.moveTo(180)

def sayTime():
	now = datetime.now()
	nowSay = "Sono le ore " + str(now.hour) + " e " + str(now.minute)
	i01.mouth.speak(nowSay)

def repeat(text):
	cutText = text[6:]
	i01.mouth.speak(cutText)

# JOYSTICK
# LEFT STICK: HEAD L/R
def StickXListener(value):

	global joyThreshold, joyGain, i01
	
	absValue = math.fabs(value)
	
	if (absValue < joyThreshold):
		i01.head.rothead.setVelocity(0)
		i01.head.rothead.moveTo(i01.head.rothead.pos)
		return
	else:
		velocity = absValue * joyGain
		i01.head.rothead.setVelocity(velocity)
		if(value < 0):
			i01.head.rothead.moveTo(i01.head.rothead.min)
		else:
			i01.head.rothead.moveTo(i01.head.rothead.max)
		return;

# LEFT STICK: HEAD U/D
def StickYListener(value):

	global joyThreshold, joyGain, i01
	
	absValue = math.fabs(value)
	
	if (absValue < joyThreshold):
		i01.head.neck.setVelocity(0)
		i01.head.neck.moveTo(i01.head.neck.pos)
		return
	else:
		velocity = absValue * joyGain
		i01.head.neck.setVelocity(velocity)
		if(value < 0):
			i01.head.neck.moveTo(i01.head.neck.max)
		else:
			i01.head.neck.moveTo(i01.head.neck.min)
		return;

# RIGHT STICK: EYES L/R
def StickRXListener(value):
	global joyThreshold, joyGain, i01
	
	absValue = math.fabs(value)
	
	if (absValue < joyThreshold):
		i01.head.eyeX.setVelocity(0)
		i01.head.eyeX.moveTo(i01.head.eyeX.pos)
		return
	else:
		velocity = absValue * joyGain
		i01.head.eyeX.setVelocity(velocity)
		if(value < 0):
			i01.head.eyeX.moveTo(i01.head.eyeX.max)
		else:
			i01.head.eyeX.moveTo(i01.head.eyeX.min)
		return;

# RIGHT STICK: EYES U/D
def StickRYListener(value):
	
	global joyThreshold, joyGain, i01
	
	absValue = math.fabs(value)
	
	if (absValue < joyThreshold):
		i01.head.eyeY.setVelocity(0)
		i01.head.eyeY.moveTo(i01.head.eyeY.pos)
		return
	else:
		velocity = absValue * joyGain
		i01.head.eyeY.setVelocity(velocity)
		if(value < 0):
			i01.head.eyeY.moveTo(i01.head.eyeY.min)
		else:
			i01.head.eyeY.moveTo(i01.head.eyeY.max)
		return;

def onJoystickInput(data):

	global xrh

	# LEFT STICK
	if (data.id == "x"):
		StickXListener(data.value)
	if (data.id == "y"):
		StickYListener(data.value)
	
	# RIGHT STICK
	if (data.id == "rx"):
		StickRXListener(data.value)
	if (data.id == "ry"):
		StickRYListener(data.value)

	# DPAD (REST = 0, UP = 0.25, RIGHT = 0.5, DOWN = 0.75, LEFT = 1.0)
	if (data.id == "pov"):
		if(data.value == 0.25):
			closeMouth()
		if(data.value == 0.75):
			openMouth()

	# X BUTTON
	if (data.id == '0' and float(data.value) == 1.0):
		relax()
		print ("Values min: ", head.rothead.min)
		print ("Values max: ", head.rothead.max)
		print ("Values pos: ", head.rothead.pos)
		print ("Values xrh: ", xrh)

	# SQUARE
	if (data.id == '2' and float(data.value) == 1.0):
		mouth.speak("ciao")

	# L TRIGGER
	if (data.id == '4' and float(data.value) == 1.0):
		startLKTracking()

	# R TRIGGER
	if (data.id == '5' and float(data.value) == 1.0):
		stopTracking()

uberjoy.addInputListener(python)
# END JOYSTICK

#	i01.setHeadVelocity(40, 40, 40)
#	i01.moveHead(80,140,120)

# i01.head.eyeY.detachPin(24)

# APPUNTI

#http://localhost:8888/api/service/i01.ear/publishText/silenzio

#https://github.com/MyRobotLab/pyrobotlab/tree/master/home/kwatters/harry/gestures/trackHumans.py
#i01.headTracking.pid.setPID("x", 35,1.0,0.1)
#i01.headTracking.pid.setPID("y", 50,1.0,0.1)