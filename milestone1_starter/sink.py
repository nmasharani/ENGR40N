# Nisha Masharani (nisham) and Luke Pappas (lpappas9)

# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random
import numpy as np


class Sink:
    def __init__(self):
        # no initialization required for sink 
        print ""
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
        
        header = recd_bits[0:18]
        src_type, payloadLength = self.read_type_size(header)
        if src_type == "txt":
            bits = recd_bits[18:18 + payloadLength + 224]
            header_symbol_stats = bits[0:224]
            frequency_map = self.read_stat(header_symbol_stats)
            encoded_bits = bits[224:]
            bits = self.huffman_decode(frequency_map, encoded_bits)
            text = self.bits2text(bits)
            print "Received the following text: "
            print text
        elif src_type == "img":
            bits = recd_bits[18:18 + payloadLength + 224] #truncate based on size
            header_symbol_stats = bits[0:224]
            encoded_bits = bits[224:]
            frequency_map = self.read_stat(header_symbol_stats)
            bits = self.huffman_decode(frequency_map, encoded_bits)
            print "Received Image"
            self.image_from_bits(bits, "rcd-image.png", payloadLength)
        else:
            bits = recd_bits[18:18 + payloadLength] #truncate based on size
            print "Received the following monotone signal: "
            print bits #monotone
        
        print ""
        return bits

    def huffman_decode(self, frequency_map, encoded_bits):
        huffman_tree_root = common_srcsink.build_huffman_tree(frequency_map)
        codeword_map = common_srcsink.build_codeword_map(huffman_tree_root)
        #for key in codeword_map:
            #print "key = " + str(key) + " and value = " + str(codeword_map[key])

        #builds the decode map by reversing the key value pairs
        decode_map = {} #{"01":0, "00101":6, "0000":7, "00111":8, "0001":9, "00100":12, "00110":13, "1":15}
        for key in codeword_map:
            decode_map[codeword_map[key]] = key

        #here is where we do the decoding
        curr_str = ""
        decoded_str = ""
        for bit in encoded_bits:
            curr_str += str(bit)
            if ((curr_str in decode_map) == True):
                symbol_val = decode_map[curr_str]
                symbol_str = str(bin(symbol_val)[2:].zfill(4))
                decoded_str += symbol_str
                curr_str = ""

        decoded_bits = np.fromstring(decoded_str, dtype=np.uint8)
        decoded_bits[:] = [x - 48 for x in decoded_bits]
        return decoded_bits
            
        
    def read_stat(self, stats):
        frequency_map = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0}
        print '\tRecieved frequency stats in header: ', stats
        print ""
        count = 0
        bitstring =""
        symbol_val = 0
        for bit in stats:
            count = count + 1
            curr_bit = str(bit)
            bitstring += curr_bit
            if count == 14:
                #symbol_str = bitstring[0:4]
                frequency_str = bitstring[0:14]
                #symbol_val = int(symbol_str, 2)
                frequency_val = int(frequency_str, 2)
                frequency_map[symbol_val] = frequency_val
                count = 0
                bitstring = ""
                symbol_val = symbol_val + 1

        return frequency_map
        
        
    #return rcd_payload

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        #bits to text impimented, tested, working LMP
        text = ""
        count = 0
        charStr = ""
        for bit in bits:
            count = count + 1
            bitStr = str(bit)
            charStr += bitStr
            if count == 8:
                asciiVal = int(charStr, 2)
                if (asciiVal >= 128 or asciiVal < 0):
                    asciiVal = 35
                char = str(unichr(asciiVal));
                text += char
                count = 0
                charStr = ""

        return  text

    def image_from_bits(self, bits,filename, payloadLength):
        # Convert the received payload to an image and save it

        # No return value required.

        img = Image.new("L", (32, 32))
        # need to get bit string into format [(r, g, b), (r, g, b), (r, g, b)]
        data = list([])
        count = 0
        intStr = ""

        # * Use this code to convert from modes that have tuples in the data list
        # * e.g., RGB mode to an image
        # * Saving this code to use in extensions

        # * rgbList = list([])

        for bit in bits:
            count += 1
            bitStr = str(bit)
            intStr += bitStr
            if count == 8:
                val = int(intStr, 2)
                data.append(val)

                # * rgbList.append(val)

                # * if (len(rgbList) == 3):
                    # * data.append(tuple(rgbList))
                    # * rgbList = list([])

                count = 0
                intStr = ""
        
        if len(data) > (1024):
            print "Bit errors caused pixel array to be too long."
            print "Trimming the pixel array to be proper length of 1024."
            data = data[0:1024]
    
        img.putdata(data)
        img.save(filename)

        pass 

            
            
    def read_type_size(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
        #this funtion is now working LMP
        # First get type
        # then convert the remaining payload size bits to string
        # convert that string to an int
        typeBits = header_bits[0:2]
        payloadLengthInBinary = header_bits[2:18]
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
        print ""
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        print ""
        return srctype, payload_length