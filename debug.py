# -*- coding: utf-8 -*- 
from __init__ import open
import os

os.system('rm ./debug/cache/*')
img2 = open('debug/ao-nang-sunset-sniskan.jpg', name=u'emil testar hej vilt med å ä och ö')
img = open('debug/ao-nang-sunset.jpg')
rotated_img = open('debug/DSC_0152.JPG')

#print img.crop().cache()
#print img2.crop().cache()
#print img.crop((16, 10)).cache()
#print img2.crop((16, 10)).cache()
#print img.crop((10, 16)).cache()
#print img2.crop((10, 16)).cache()
#print img2.crop((10,16)).img()

rotated_img.crop((10,16)).constrain(100, 160).save("debug/test.jpg")
