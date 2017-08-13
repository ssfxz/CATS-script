import os
import time
from PIL import Image

while 1:
	os.popen("adb shell /system/bin/screencap -p /storage/0000-0000/screenshot.png");
	os.popen("adb pull /storage/0000-0000/screenshot.png .");

	image = Image.open("./screenshot.png");
	# image.show();
	
	if image.getpixel((1800, 1300)) == (231, 217, 203, 255):
		os.popen("adb shell input tap 1500 1400");
		print("fight");
	elif image.getpixel((300, 215)) == (255, 255, 255, 255):
		os.popen("adb shell input tap 2300 400");
		print("action");
	elif image.getpixel((1310, 1310)) == (210, 35, 37, 255):
		os.popen("adb shell input tap 1300 1400");
		print("done");
	
	print("sleep");
	time.sleep(1);