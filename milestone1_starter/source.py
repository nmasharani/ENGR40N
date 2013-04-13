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
                payload = self.bits_from_image(self.fname)
                header = self.get_header(payload.shape[0], "img")
            else:           
                payload = self.text2bits(self.fname) 
                header = self.get_header(payload.shape[0], "txt")         
        else:
            #added the functionality to make monotone, tested and works
            payload = np.ones(self.monotone, dtype=np.uint8)
            header = self.get_header(self.monotone, "mon")
                
        #this makes the databits to be the header + payload, tested and works
        databits = np.append(header, payload);
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
        # monotone 00
        # image 01
        # text is 10
        headerstr = ""
        if srctype == "img":
            headerstr += "01"
        elif srctype == "txt":
            headerstr += "10"
        else:
            #monotone
            headerstr += "00"
        headerstr += bin(payload_length)[2:].zfill(32)
        header = np.fromstring(headerstr, dtype=np.uint8)
        header[:] = [x - 48 for x in header]
        return header
