import os
import time
import pytesseract
from PIL import Image

ATK = 365;

image = Image.open("./screenshot.png");
box = (1300, 150, 1550, 270);
region = image.crop(box);
region.save('tmp1.png')

region2 = region.convert("1");
region2.save('tmp2.png');

print pytesseract.image_to_string(region2)
