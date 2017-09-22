#coding:utf-8
import os
import time

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

def getScreenPixel(pos):
	print "\t\tbegin screenshot..."
	# print pos
	# pos = (1,1)
	offset = (pos[1] * 2560 + pos[0]) * 4
	adb("shell ./system/bin/screencap | hexdump -C -s %s -n 4 > ./color" % (12 + offset))
	colorFile = open("color", "rw+")
	colorFile.seek(10, 0)
	colorR = int('0x' + colorFile.read(2), 16)
	colorFile.seek(1, 1)
	colorG = int('0x' + colorFile.read(2), 16)
	colorFile.seek(1, 1)
	colorB = int('0x' + colorFile.read(2), 16)
	# print "Color: %s %s %s" % (colorR, colorG, colorB)
	print "\t\tfinish fetch screenshot."
	return (colorR, colorG, colorB, 255);

def startFastFight():
	adb("shell input tap 1400 1300")

def willWin(): #敌方血条左端
	return getScreenPixel((1570, 210)) == (255, 255, 255, 255)

def goFighting():
	adb("shell input tap 1200 600")

def skipFighting():
	adb("shell input tap 2400 1300")

#def stillFighting():
#	not getScreenPixel((300, 200)) == (255, 255, 255, 255)

def clickConfirmed():
	adb("shell input tap 1300 1400")

states = {
	"Home": {
		"prepare": lambda: withSleep(0.1, sleepUntil(lambda : getScreenPixel((1800, 1300)) == (231, 217, 203, 255))), #右上角设置按钮圆圈上端
		"decide": lambda: "startFastFight",
		"choices": {
			"startFastFight": {
				"action": startFastFight,
				"nextState": "PreFighting"
			}
		}
	},
	"PreFighting": {
		"prepare": lambda: withSleep(0.1, sleepUntil(lambda : getScreenPixel((300, 215)) == (255, 255, 255, 255))), #我方血量个位数字顶端
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
		"prepare": lambda: withSleep(0.1, sleepUntil(lambda : getScreenPixel((1310, 1310)) == (210, 35, 37, 255))), #我方血量个位数字顶端
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
