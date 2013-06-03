import math
import common_txrx as common
import numpy as np
import hamming_db as hamming

class Transmitter:
    def __init__(self, carrier_freq, samplerate, one, spb, silence, cc_len):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence
        self.cc_len = cc_len
        print ""
        print ""
        print 'Transmitter: '
        print ""

    '''
    def __init__(self, carrier_freq, samplerate, one, spb, silence):
        self.fc = carrier_freq  # in cycles per sec, i.e., Hz
        self.samplerate = samplerate
        self.one = one
        self.spb = spb
        self.silence = silence

        print ""
        print ""
        print 'Transmitter: '
        print ""
    '''

    def add_preamble(self, databits):
        '''
        Prepend the array of source bits with silence bits and preamble bits
        The recommended preamble bits is 
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        The output should be the concatenation of arrays of
            [silence bits], [preamble bits], and [databits]
        '''
        # fill in your implementation

        preamble = common.get_Preamble()
        print "\tSent preamble: " + str(preamble)
        databits_with_preamble = np.concatenate((np.zeros(self.silence), preamble, databits), axis=0)
        return databits_with_preamble


    def bits_to_samples(self, databits_with_preamble):
        '''
        Convert each bits into [spb] samples. 
        Sample values for bit '1', '0' should be [one], 0 respectively.
        Output should be an array of samples.
        '''
        samples = list([])

        for bit in databits_with_preamble:
            if (bit == 1):
                for i in range(0,self.spb):
                    samples.append(self.one)
            else:
                for i in range(0,self.spb):
                    samples.append(0.0)

        print "\tNumber of samples being sent: " + str(len(samples))

        return np.array(samples)
        

    def modulate(self, samples):
        '''
        Calls modulation function. No need to touch it.
        '''
        return common.modulate(self.fc, self.samplerate, samples)

    def encode(self, databits):
        index, coded_data = self.hamming_encoding(databits, False)
        print "\tlength before coding: " + str(len(databits))
        print "\tlength after coding: " + str(len(coded_data))

        # first 30 bits: size 
        # next 2 bits: coding rate
        header = bin(index)[2:].zfill(2)

        header_len, header_index = common.get_coding_header_info()

        coded_len = len(coded_data) + header_len * 3

        header = bin(coded_len)[2:].zfill(30) + header
        header_arr = np.fromstring(header, dtype=np.uint8)

        header_arr[:] = [x - ord('0') for x in header_arr] 

        print "\tcoding header: " + str(header_arr)

        header_index, coded_header = self.hamming_encoding(header_arr, True)

        coded_bits = np.concatenate((coded_header, coded_data), axis=0)
        return coded_bits

    
    def hamming_encoding(self, databits, is_header):
        n,k,index,G = 0,0,0,[0]
        if (is_header):
            n,k,index,G = hamming.gen_lookup(3)
        else:
            n,k,index,G = hamming.gen_lookup(self.cc_len)

        if (len(databits) % k) != 0:
            padding = (k - (len(databits) % k)) * [0]
            databits = np.concatenate((databits, padding), axis=0)

        len_databits = len(databits)

        databits_k = np.array([databits[i:i+k] for i in range(0, len_databits, k)])

        databits_k_len = len(databits_k)

        coded_bits = list([])
        for i in range(0, databits_k_len):

            coded_fragment = np.dot(databits_k[i][:], G)

            coded_bits.append(coded_fragment)

        coded_bits = np.array(coded_bits)
        coded_bits = coded_bits.flatten()

        return index, coded_bits

