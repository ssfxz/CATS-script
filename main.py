import os  
import time  


os.popen("adb shell /system/bin/screencap -p /storage/0000-0000/screenshot.png");  
os.popen("adb pull /storage/0000-0000/screenshot.png .");  