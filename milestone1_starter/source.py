# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random
import numpy as np



class Source:
    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        print 'Source: '

    def process(self):
        # Form the databits, from the filename 
        if self.fname is not None:
            if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                databits = self.bits_from_image(self.fname)
            else:           
                databits = self.text2bits(self.fname)          
        else: 
        # test              
            return 0, 0  

        payload = databits
        return payload, databits

    def text2bits(self, filename):
        
        f = open(filename, 'r')
        fileStr = f.read()

        # http://stackoverflow.com/questions/8452961/convert-string-to-ascii-value-python
        ascii = np.array([ord(c) for c in fileStr], dtype=np.uint8)

        bits = np.unpackbits(ascii)

        return bits

    def bits_from_image(self, filename):
   
        img = Image.open(filename)
        # img.mode() must equal "RGB" for this specific code to work
        img = img.convert("RGB")

        # gives a list of rgb values in the form { (R, G, B) , (R, G, B) , (R, G, B) }
        pixels = list(img.getdata())

        pixlist = list([])
        for t in pixels:
            for x in t:
                pixlist.append(x)

        # converts to numpy array
        array = np.array(pixlist, dtype=np.uint8) 

        # converts to numpy bit array
        bits = np.unpackbits(array) 
        np.set_printoptions(threshold='nan')

        return bits

    def get_header(self, payload_length, srctype): 
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        return header
