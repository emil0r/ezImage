# -*- coding: utf-8 -*- 
from __init__ import open
import os

os.system('rm ./debug/cache/*')
img2 = open('debug/ao-nang-sunset-sniskan.jpg', name=u'emil testar hej vilt med å ä och ö')
img = open('debug/ao-nang-sunset.jpg')
rotated_img = open('debug/DSC_0152.JPG')
elin = open(u'/Users/emil/dev/web/ecms/ecms_root/media/images/v\xe4xtst\xf6d/Elin, tv\xe5 sektioner 2009-06-25 12-37-14 [800x600].JPG')

#print img.crop().cache()
#print img2.crop().cache()
#print img.crop((16, 10)).cache()
#print img2.crop((16, 10)).cache()
#print img.crop((10, 16)).cache()
#print img2.crop((10, 16)).cache()
#print img2.crop((10,16)).img()

#rotated_img.crop((10,16)).constrain(100, 160).save("debug/test.jpg")
elin.crop((10,16)).constrain(100,160).save("debug/elin.jpg")
