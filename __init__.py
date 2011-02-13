import Image
from hashlib import md5
import os
import os.path
import urllib

try:
    from django.conf import settings
    IMAGECACHE_DIR = settings.media_root + 'cache/images/'
    IMAGECACHE_WEB = settings.media_url + 'cache/images/'
except:
    IMAGECACHE_DIR = os.getcwd() + '/debug/cache/'
    IMAGECACHE_WEB = '/debug/cache/'

CACHE = dict()

__doc__ = """
Image wrapper around pil for distort, constrain, crop and pad. Adds caching on top.
Author: Emil Bengtsson <emil@emil0r.com>
"""


def open(infile, name=None, mode = "r"):
    
    if isinstance(infile, file):
        path = infile.name
    else:
        path = infile
    try:
        if type(path) == unicode:
            path = path.encode('utf-8')
        format = path.rsplit('.',1)[1].lower()
        return ezImage(path, mode, format, name)
    except Exception as e:
        return None

class ezImage:
    def __init__(self, path, mode, format, name=None):
        
        self.path = path
        self.name = '.'.join(''.join(path.split(os.sep)[-1:]).split('.')[:-1]) if name == None else name
        self.mode = mode
        self.format = format
        self.commands = []
        if type(self.name): self.name = self.name.encode('utf-8')

    def distort(self, width = 100, height = 100, imagefilter = Image.ANTIALIAS):
        self.commands.append(
            ['distort',
            {
            'width': width,
            'height': height,
            'imagefilter': imagefilter
            }])
        return self
    def constrain(self, width = 100, height = 100, imagefilter = Image.ANTIALIAS):
        self.commands.append(
            ['constrain',
             {
            'width': width,
            'height': height,
            'imagefilter': imagefilter
            }])
        return self
    def crop(self, rectangle=()):
        self.commands.append(
            ['crop',
            {
            'rectangle': rectangle
            }])
        return self
    def pad(self, padding = None, color = (255,255,255,255)):
        self.commands.append(
            ['pad',
             {
            'padding': padding,
            'color': color
            }])
        return self
    def _distort(self, width = 100, height = 100, imagefilter = Image.ANTIALIAS):
        self.pilimg = self.pilimg.resize((width, height), imagefilter)
        
        return self
    
    def _constrain(self, width = 100, height = 100, imagefilter = Image.ANTIALIAS):
        self.pilimg.thumbnail((width, height), imagefilter)

        return self
    
    def _crop(self, rectangle):
        """
    	rectangle = left, top, right, bottom
        """
        if len(rectangle) == 0:
            w, h = self.pilimg.size
            if w > h:
                dif = (int)((w - h)/2.0)
                rectangle = (dif, 0, h + dif, h)
            else:
                dif = (int)((h - w)/2.0)
                rectangle = (0, dif, w, w + dif)
        elif len(rectangle) == 2:
            w, h = self.pilimg.size
            ratio = float(rectangle[0]) / float(rectangle[1])
            x, y, width, height = 0, 0, 0, 0
            if w > h:
                if ratio > 1.0:
                    height = (int)(w / ratio)
                    width = w
                    x = 0
                    y = (int)((h - height) / 2.0)
                    height += y
                else:
                    width = (int)(h * ratio) + x
                    height = h
                    x = (int)((w - width) / 2.0)
                    y = 0
                    width += x
            else:
                if ratio > 1.0:
                    width = w
                    height = (int)(w / ratio) + y
                    x = 0
                    y = (int)((h - height) / 2.0)
                    height += y
                else:
                    height = h
                    width = (int)(h * ratio) + x
                    x = (int)((w - width) / 2.0)
                    y = 0
                    width += x
            rectangle = (x, y, width, height)
        print rectangle 
        self.pilimg = self.pilimg.crop(rectangle)    
        return self
    
    def _pad(self, padding = None, color = (255,255,255,255)):
        """
        padding: left, top, right, bottom. Values can't be below 0.
        color: colors depending on the mode, defaults to white and opaque
        """
        if padding == None:
            top = bottom = left = right = 0
            if self.pilimg.size[0] > self.pilimg.size[1]:
                top = (self.pilimg.size[0] - self.pilimg.size[1]) / 2
                bottom = top
                while bottom + top + self.pilimg.size[1] < self.pilimg.size[0]:
                    bottom += 1
            else:
                left = (self.pilimg.size[1] - self.pilimg.size[0]) / 2
                right = left
                while left + right + self.pilimg.size[0] < self.pilimg.size[1]:
                    right += 1
            padding = (left, top, right, bottom)
            
        if len(padding) == 4:
            for p in padding:
                if p < 0:
                    return self
            
            w = self.pilimg.size[0] + padding[0] + padding[2]
            h = self.pilimg.size[1] + padding[1] + padding[3]
            tmp = Image.new(self.pilimg.mode, (w,h), color)
            tmp.paste(self.pilimg, (padding[0], padding[1], self.pilimg.size[0] + padding[0], self.pilimg.size[1] + padding[1]))
            del self.pilimg
            self.pilimg = tmp
            
        return self

    def _gethash(self):
        try:
            return md5( '{size}{time}{path}{commands}'.format(size=os.path.getsize(self.path), time=os.path.getmtime(self.path), path=self.path, commands=self.commands)).hexdigest()
        except UnicodeDecodeError as e:
            pass

    def size(self):
        hashmd5 = self._gethash()
        path = '{dir}{hash}.{format}'.format(dir=IMAGECACHE_DIR, hash=hashmd5, format=self.format)
        if os.path.isfile(path):
            return os.path.getsize(path)
        
        result = self._execute()
        if result:
            size = self.pilimg.size
            del self.pilimg
            return size
        return 0

    def _execute(self):
        try:
            if not hasattr(self, "pilimg"):
                self.pilimg = Image.open(self.path, self.mode)
        except Exception as e:
            return False
        for command in self.commands:
            method = getattr(self, "_" + command[0])
            method(**command[1])
        return True

    def _sanitize_name(self, url=False):
        if not url:
            return self.name.replace(' ', '-')
        return urllib.quote(self.name.replace(' ', '-'))

    def img(self, alt='', title='', use_name=True):
        hashmd5 = self._gethash()
        if alt == '' and use_name: alt = self.name
        if title == '' and use_name: title = self.name
        if hashmd5 not in CACHE:
            self.cache()
        return '<img src="{src}" alt="{alt}" title="{title}" />'.format(src=CACHE[hashmd5].webpath, alt=alt, title=title)
    
    def cache(self):
        hashmd5 = self._gethash()

        if hashmd5 in CACHE:
            return CACHE[hashmd5].webpath
        else:
            # needs to be utf-8
            hdpath = '{dir}{name}-{hash}.{format}'.format(dir=IMAGECACHE_DIR, name=self._sanitize_name(), hash=hashmd5, format=self.format)
            webpath = '{web}{name}-{hash}.{format}'.format(web=IMAGECACHE_WEB, name=self._sanitize_name(True), hash=hashmd5, format=self.format)
            if not os.path.isfile(hdpath):
                success = self._execute()
                if not success:
                    return None
                self.pilimg.save(hdpath)
                del self.pilimg

            self.webpath = webpath
            self.hdpath = hdpath


            CACHE[hashmd5] = self
            return webpath
            
