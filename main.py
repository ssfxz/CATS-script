import os
import time
from PIL import Image

ATK = 365;

while 1:
	os.popen("adb shell /system/bin/screencap -p /storage/0000-0000/screenshot.png");
	os.popen("adb pull /storage/0000-0000/screenshot.png .");

	image = Image.open("./screenshot.png");
	# image.show();

	if image.getpixel((1800, 1300)) == (231, 217, 203, 255):
		os.popen("adb shell input tap 1500 1400");
		print("start");

	elif image.getpixel((300, 215)) == (255, 255, 255, 255):
		# box = (1300, 150, 1550, 270);
		# region = image.crop(box);
		# outfile = 'tmp1.png'
		# region.save(outfile)

		if image.getpixel((1570, 210)) == (255, 255, 255, 255) :
			os.popen("adb shell input tap 2300 400");
			print("Fight");
		else :
			os.popen("adb shell input tap 2400 1400");
			print("Skip");

	elif image.getpixel((1310, 1310)) == (210, 35, 37, 255):
		os.popen("adb shell input tap 1300 1400");
		print("done");

	# print("sleep");
	# time.sleep(0.5);
	# print("week up");
