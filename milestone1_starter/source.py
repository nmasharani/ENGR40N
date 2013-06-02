# Nisha Masharani (nisham) and Luke Pappas (lpappas9)

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
        # Notes:
        #1. pre_payload = the oringinal, uncompressed source bits
        #2. payload = the compressed bits that will be transmitted
        #3. symbol_frequency_dict = the dictionary mapping symbol values to frequencies
        #4. header = the header for the transmitted bits. if image or text, 
        if self.fname is not None:
            if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                pre_payload = self.bits_from_image(self.fname)
                source_bits = pre_payload
                payload, symbol_frequency_dict = self.huffman_encode(pre_payload)
                header = self.get_huffman_header(payload.shape[0], "img", symbol_frequency_dict) #note that shape[0] returns the length of the payload array. 
                # refer to http://stackoverflow.com/questions/10200268/python-what-does-shape-do-in-for-i-in-rangey-shape0 if necessary for shape[0]
            else:           
                pre_payload = self.text2bits(self.fname)
                source_bits = pre_payload
                payload, symbol_frequency_dict = self.huffman_encode(pre_payload) 
                header = self.get_huffman_header(payload.shape[0], "txt", symbol_frequency_dict)
    
        else:
            #added the functionality to make monotone, tested and works
            payload = np.ones(self.monotone, dtype=np.uint8)
            source_bits = payload
            header = self.get_header(self.monotone, "mon")
                
        #this makes the databits to be the header + payload, tested and works
        databits = np.append(header, payload);
        #process is now going to return the orignial source bits(payload) and then
        # return the header+huffman encoded bits as well. 
        return source_bits, databits 






    def huffman_encode(self, original_payload):
        #initialize the dictionary to zro for all possible symbols, where the symblos are the keys in the dictionary, listed under their integer equivalents (ie 1111 would be listed under 15)
        symbol_frequency_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0}
        #then process each 4 bit symbol at a time, and update corresponding
        # value in the dictionary by one. 
        symbol_length = 4
        count = 0
        symbol_str = ""
        for bit in original_payload:
            count = count + 1
            bitStr = str(bit)
            symbol_str += bitStr
            if count == symbol_length:
                val = int(symbol_str, 2)
                symbol_frequency_dict[val] = symbol_frequency_dict[val] + 1
                count = 0
                symbol_str = ""

        #have the frequencies, now I need to build the huffman encoding
        # and return a dictionary mapping symbols (4 bit strings as int values) to codeword strings. 
        print "source: frequency map:"
        for key in symbol_frequency_dict:
            print "key = " + str(key) + " and val = " + str(symbol_frequency_dict[key])
        huffman_tree_root = common.build_huffman_tree(symbol_frequency_dict)
        codeword_map = common.build_codeword_map(huffman_tree_root)

        #now I compress the orignial bit string by replacing every 4 bit symbol
        # with its corresponding huffman code_word
        count = 0
        curr_symbol_str = ""
        compressed_string = ""
        for bit in original_payload:
            count = count + 1
            curr_bit = str(bit)
            curr_symbol_str += curr_bit
            if count == symbol_length:
                val = int(curr_symbol_str, 2)
                code_word = codeword_map[val]
                compressed_string += code_word
                count = 0
                curr_symbol_str = ""

        # now turn the string into an array of bits
        compressed_bits_list = list([])
        cmpressed_string_len = len(compressed_string)
        for i in range(0,cmpressed_string_len):
            bit_val = int(compressed_string[i], 2)
            compressed_bits_list.append(bit_val)

        compresssed_bit_array = np.array(compressed_bits_list)
        return compresssed_bit_array, symbol_frequency_dict
    






    def text2bits(self, filename):
        f = open(filename, 'r')
        fileStr = f.read()

        # http://stackoverflow.com/questions/8452961/convert-string-to-ascii-value-python
        ascii = np.array([ord(c) for c in fileStr], dtype=np.uint8)
        bits = np.unpackbits(ascii)
        return bits








    def bits_from_image(self, filename):
        img = Image.open(filename)

        # img.mode() must equal "L" for decoding to work
        img = img.convert("L")
        
        pixels = list(img.getdata())
        array = np.array(pixels, dtype=np.uint8) 

        # Use this code to convert from modes that have tuples in the data list
        # e.g., RGB mode to a numpy array
        # Saving this code to use in extensions
        
        """
        pixlist = list([])
        for t in pixels:
            for x in t:
                pixlist.append(x)
        # converts to numpy array
        array = np.array(pixlist, dtype=np.uint8) 
        """
        # converts to numpy bit array
        bits = np.unpackbits(array) 
        np.set_printoptions(threshold='nan')
        return bits







    def get_huffman_header(self, payload_length, srctype, frequency_map):
        headerstr = ""
        if srctype == "img":
            headerstr += "01"
        else:
            headerstr += "10"
        headerstr += bin(payload_length)[2:].zfill(16)
        # NOTE THAT THE HEADER IS 2 BITS TO ENCODE FILE TYPE
        # THEN 16 BITS FOR PAYLOAD LENGTH
        # THEN 160 BITS ENCODING THE SYMBOL FREQUENCIES
        # SYMBOLS AND FREQUENCIES ARE STORED TOGETHER IN 10 TOTAL BITS FOR EACH SYMBOL FREQUENCY PAIR
        # FIRST FOUR BITS ENCODE THE SYMBOL INT VAL, LAST 6 BITS ENCODE THE FREQUENCY OF THE SYMBOL. 
        for key in frequency_map:
            code_word_str = str(bin(frequency_map[key])[2:].zfill(10))
            key_val_str = str(bin(key)[2:].zfill(4))
            headerstr += (key_val_str + code_word_str)

        header = np.fromstring(headerstr, dtype=np.uint8)
        header[:] = [x - 48 for x in header]
        print "header = " 
        print header
        return header







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
        headerstr += bin(payload_length)[2:].zfill(16)
        header = np.fromstring(headerstr, dtype=np.uint8)
        header[:] = [x - 48 for x in header]
        print "header = " 
        print header
        return header
