import math
import time

pinRothead = 13

rotheadMin = 30  # sx
rotheadMax = 160 # dx

rotheadRest = 95
rotheadVelocity = 45

leftPort = "COM5"

i01 = Runtime.create("i01", "InMoov")

left = Runtime.createAndStart("i01.left", "Arduino")
left.connect(leftPort)

head = Runtime.create("i01.head","InMoovHead")
head.rothead.setVelocity(rotheadVelocity)
head.rothead.map(0, 180, rotheadMin, rotheadMax)
head.rothead.setSpeedControlOnUC(False)

i01.startHead(leftPort)
i01.head.rothead.attach(left, pinRothead)

i01.head.rothead.sweep(i01.head.rothead.min, i01.head.rothead.max, 30, -1, False)
