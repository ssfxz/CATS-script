#coding:utf-8
import os
import time
from PIL import Image

### general tools

def adb(cmd):
	return os.popen("adb " + cmd)

def sleepUntil(p):
	while not p():
		pass

def doNothing():
	pass

def withSleep(t, action):
	def inner():
		time.sleep(t) #单位: 秒
		return action()
	return inner

### game logic

lastImage = None

def getScreen():
	print "\t\tbegin screenshot..."
	# adb("shell ./system/bin/screencap -p ./storage/sdcard1/screenshot.png");
	# print "\t\tfinish screenshot."
	# adb("pull ./storage/sdcard1/screenshot.png .");
	adb("shell ./system/bin/screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > screenshot.png");
	# adb("shell ./system/bin/screencap > screenshot.bmp");
	print "\t\tfinish fetch screenshot."

	image = Image.open("./screenshot.png");
	#image.show();
	lastImage = image
	return image

def startFastFight():
	adb("shell input tap 1400 1300")

def willWin(): #敌方血条左端
	img = getScreen()
	return img.getpixel((1570, 210)) == (255, 255, 255, 255)

def goFighting():
	adb("shell input tap 1200 600")

def skipFighting():
	adb("shell input tap 2400 1300")

#def stillFighting():
#	not getScreen().getpixel((300, 200)) == (255, 255, 255, 255)

def clickConfirmed():
	adb("shell input tap 1300 1400")

states = {
	"Home": {
		"prepare": lambda: withSleep(0.5, sleepUntil(lambda : getScreen().getpixel((1800, 1300)) == (231, 217, 203, 255))), #右上角设置按钮圆圈上端
		"decide": lambda: "startFastFight",
		"choices": {
			"startFastFight": {
				"action": startFastFight,
				"nextState": "PreFighting"
			}
		}
	},
	"PreFighting": {
		"prepare": lambda: withSleep(0.5, sleepUntil(lambda : getScreen().getpixel((300, 215)) == (255, 255, 255, 255))), #我方血量个位数字顶端
		"decide": lambda: "goFighting" if willWin() else "skipFighting",
		"choices": {
			"goFighting": {
				"action": goFighting,
				"nextState": "Fighting"
			},
			"skipFighting": {
				"action": skipFighting,
				"nextState": "PreFighting"
			}
		}
	},
	"Fighting": {
		"prepare": lambda: (),
		"decide": lambda: "doNothing",
		"choices": {
			"doNothing": {
				"action": doNothing,
				"nextState": "Confirm"
			}
		}
	},
	"Confirm": {
		"prepare": lambda: withSleep(0.5, sleepUntil(lambda : getScreen().getpixel((1310, 1310)) == (210, 35, 37, 255))), #我方血量个位数字顶端
		"decide": lambda: "confirmed",
		"choices": {
			"confirmed": {
				"action": clickConfirmed,
				"nextState": "Home"
			}
		}
	}
}
InitState = "Home"

### auto machine

st = InitState
while True:
	print "State: %s\n\tpreparing..." % (st)
	states[st]["prepare"]()
	print "\tprepared."
	decision = states[st]["decide"]()
	print "Decision: %s" % (decision)
	choice = states[st]["choices"][decision]
	choice["action"]()
	st = choice["nextState"]
