import time, math
from random import randint
from datetime import datetime
from threading import Thread

# execfile('/home/scognito/dev/git/MRL/scripts/qwerty_tablet.py')

song1Path = "/home/scognito/Music/blink.mp3";
song2Path = "/home/scognito/Music/amy.mp3";
song3Path = "/home/scognito/Music/ramones.mp3";
song4Path = "/home/scognito/Music/sultan.mp3";

leftPort = "/dev/ttyACM0"

joystickIndex = 0;

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
eyeXvelocity = 100 # -1 full speed
eyeYvelocity = 100
neckVelocity = 45
rotheadVelocity = 45

headVelocity = 45
eyesVelocity = 45
joyThreshold = 0.5

#voice="cmu-bdl-hsmm"
voice="istc-lucia-hsmm"
#voice="Italian_Francesco"

#music
maxSongs = 4
curSong = 0

mouth = Runtime.createAndStart("i01.mouth", "MarySpeech")
#mouth = Runtime.createAndStart("i01.mouth", "NaturalReaderSpeech")
mouth.setVoice(voice)

playAudio = Runtime.createAndStart("i01.playAudio", "NaturalReaderSpeech")

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
uberjoy.addInputListener(python)

head = Runtime.create("i01.head","InMoovHead")

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

head.setAutoDisable(True)
python.subscribe("i01.ear","recognized") #FIX
ear = i01.ear
ear.setLanguage("it-IT")
ear.startListening()

def relax():
	playAudio.audioFile.silence()
	#i01.mouth.speak("va bene.")
	i01.head.eyeX.moveTo(eyeXrest)
	i01.head.eyeY.moveTo(eyeYrest)
	i01.head.neck.moveTo(neckRest)
	i01.head.rothead.moveTo(rotheadRest)
	i01.head.jaw.moveTo(0)

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
	elif (text == u"musica"):
		startMp3()
	elif (text == u"silenzio"):
		stopMp3()
	elif (text == u"che ore sono"):
		sayTime()
	elif (text.startswith("ripeti")):
		repeat(text)
	
def startMp3():
	playAudio.audioFile.silence()
	time.sleep(1)

	global curSong, maxSongs

	if(curSong == maxSongs - 1):
		curSong = 0
	
	#curSong = randint(0, 3)
	if (curSong == 0):
		mouth.speakBlocking("Riproduco i blinc 182")
		playAudio.audioFile.playFile(song1Path, False)
	elif (curSong == 1):
		mouth.speakBlocking("Riproduco emi uainaus")
		playAudio.audioFile.playFile(song2Path, False)
	elif (curSong == 2):
		mouth.speakBlocking("Riproduco i ramones")
		playAudio.audioFile.playFile(song3Path, False)
	elif (curSong == 3):
		mouth.speakBlocking("Riproduco i dair streits")
		playAudio.audioFile.playFile(song4Path, False)

	curSong = curSong+1
#	audioFile = Runtime.createAndStart("af1", "AudioFile");
#	audioFile.playFile("my.mp3" False); # autostart

def stopMp3():
	playAudio.audioFile.silence()
    
def rotateRight():
	i01.head.rothead.moveTo(0)
  
def rotateLeft():
	i01.head.rothead.moveTo(180)

def suca():
	i01.mouth.speak("vafanculo coglione")
	
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

def sayTime():
	now = datetime.now()
	nowSay = "Sono le ore " + str(now.hour) + " e " + str(now.minute)
	i01.mouth.speak(nowSay)

def repeat(text):
	cutText = text[6:]
	i01.mouth.speak(cutText)

# JOYSTICK
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
		if (value < 0):
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
	if ((data.id == "1" or data.id == "B") and float(data.value) == 1.0):
		disableServos()
	
	if ((data.id == "X") and float(data.value) == 1.0):
		openMouth()

	if ((data.id == "Y") and float(data.value) == 1.0):
		closeMouth()

	if ((data.id == "A") and float(data.value) == 1.0):
		relax()

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