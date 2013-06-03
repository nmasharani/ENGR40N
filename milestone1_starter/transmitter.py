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
        print "length before coding: " + str(len(databits))
        print "length after coding: " + str(len(coded_data))

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

        n,k,H = hamming.parity_lookup(index)

        # split coded bits into chunks of size n (k message + (n-k) parity)
        len_coded_bits = len(coded_bits)
        coded_bits_split = [coded_bits[i:i+n] for i in range(0,len_coded_bits,n)]

        len_coded_bits_split = len(coded_bits_split)

        decoded_bits = list([])

        zero_syndrome = np.zeros(n-k, dtype=int)
        HT = np.transpose(H)

        num_errors = 0

        for i in range(0, len_coded_bits_split):
            syndrome = np.dot(H, np.transpose(coded_bits_split[i]))
            syndrome[:] = [x % 2 for x in syndrome]
            # syndrome is all zeros: no errors
            if np.array_equal(syndrome, zero_syndrome):
                decoded_bits.append(coded_bits_split[i][0:k])


            # if there's an error
            else:
                print "syndrome " + str(syndrome)

                error_loc = -1
                # figure out which column of H the syndrome corresponds with
                for j in range(0, k):
                    if np.array_equal(HT[j], syndrome):
                        error_loc = j
                        break
                # only care about errors in the message bits, not in the parity bits
                if error_loc < 0:
                    decoded_bits.append(coded_bits_split[i][0:k])
                
                # decode by flipping the correct bit
                else:
                    print "syndrome = " + str(syndrome)
                    cur_decoded = coded_bits_split[i][0:k]
                    
                    if (cur_decoded[error_loc] == 1):
                        cur_decoded[error_loc] = 0
                    else:
                        cur_decoded[error_loc] = 1
                    
                    decoded_bits.append(cur_decoded)
                    num_errors += 1


        if (is_header):
            print "header errors corrected: " + str(num_errors)
        else:
            print "errors corrected: " + str(num_errors)

        decoded_bits = np.array(decoded_bits)

        return index, coded_bits

