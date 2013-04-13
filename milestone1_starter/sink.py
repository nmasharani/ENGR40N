# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random


class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        # If its an image, save it as "rcd-image.png"
        # If its a text, just print out the text
        
        # Return the received payload for comparison purposes
        
        #1. split numpy array inot header and payload
        #2. get type from header
        #3. get size of payload from header
        #4. truncate payload corresponding to size
        #5. convert the payload array of 1's and 0's to image or text
        # based on the header info.
        
        header = recd_bits[0:11]
        type, payloadLength = self.read_header(header)
        
        
        print header
        
        
        
    #return rcd_payload

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        return  text

    def image_from_bits(self, bits,filename):
        # Convert the received payload to an image and save it
        # No return value required .
        pass 

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        #this funtion is now working LMP
        # First get type
        # then convert the remaining payload size bits to string
        # convert that string to an int
        typeBits = header_bits[0:2]
        payloadLengthInBinary = header_bits[2:34]
        if typeBits[0] == 1:
            srctype = "txt"
        elif typeBits[1] == 1:
            srctype = "img"
        else:
            srctype = "mon"
    
        payloadLengthString = ""
        for bit in payloadLengthInBinary:
            bitStr = str(bit)
            payloadLengthString += bitStr
        payload_length = int(payloadLengthString, 2);
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length