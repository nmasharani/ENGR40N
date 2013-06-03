import sys
import math
import numpy
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3
import hamming_db as hamming

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble 
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb 
        print ""
        print ""
        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        ''' 
        return receiver_mil3.detect_threshold(demod_samples)

    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        
        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''

        numpy.set_printoptions(threshold=numpy.nan)

        #print demod_samples

        energy_offset = -1

        demod_samples_length = len(demod_samples)
        for i in range(0, demod_samples_length - self.spb):
            cur_samples = demod_samples[i:i+self.spb]
            average_samples = cur_samples[self.spb/4 : self.spb * 3 / 4]
            average = sum(average_samples) / len(average_samples)
            if (average >= (one + thresh)/2):
                energy_offset = i
                break

        print "energy offset " + str(energy_offset)

        if energy_offset < 0:
            print ""
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            print ""
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''
        # Fill in your implementation of the cross-correlation check procedure

        preamble = common.get_Preamble()

        preamble_len = len(preamble)
        preamble_samples = common.get_Preamble_Samples(self.spb, preamble, one)

        # Fill in your implementation of the high-energy check procedure

        correlation = list([])

        # range will go through the entire array of demodulated samples, stopping
        # when the remaining bits is too short to be the preamble

        preamble_samples_length = len(preamble_samples)
        for i in range (energy_offset, demod_samples_length - preamble_samples_length):
            current_range = demod_samples[i:i + preamble_samples_length]
            dot = numpy.dot(current_range, preamble_samples)
            norm = LA.norm(current_range)
            if norm != 0:
                correlation.append(dot/norm)

        maxindex = numpy.argmax(numpy.array(correlation))

        preamble_offset = maxindex
        print "Max Correlation Value: " + str(correlation[maxindex])
        print "Preamble offset: " + str(preamble_offset)
        #print preamble_offset
         # fill in the result of the cross-correlation check 
        
        '''
        [preamble_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]). 
        Note that the final return value is [offset + pre_offset]
        '''

        return energy_offset + preamble_offset

    

    def demap_and_check(self, demod_samples, preamble_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit values of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not terminate the program. 
        Output is the array of data_bits (bits without preamble)
        '''

        databits_list = list([])
        preamble = common.get_Preamble()
        preamble_len = len(preamble)
        thresh_one = list([])
        thresh_zero = list([])

        for i in range(0, preamble_len):
            sample_index = i * self.spb + preamble_start
            cur_samples = demod_samples[sample_index:sample_index + self.spb]
            average_samples = cur_samples[self.spb/4 : self.spb * 3 / 4]
            average = sum(average_samples) / len(average_samples)
            if (preamble[i] == 1):
                thresh_one.append(average)
            else:
                thresh_zero.append(average)

        #Update the one, zero, and thresh values
        one = sum(thresh_one) / float(len(thresh_one))
        zero = sum(thresh_zero) / float(len(thresh_zero))
        thresh = (one + zero) / 2.0
        print ""
        print "\t0/1 threshold: " + str(thresh)
        print "\tone: " + str(one)
        print "\tzero: " + str(zero)
        print ""

        bits = list([])

        demod_samples_length = len(demod_samples)
        for i in range(preamble_start, demod_samples_length, self.spb):
            cur_samples = demod_samples[i:i + self.spb]
            if (len(cur_samples) < self.spb):
                break
            average_samples = cur_samples[self.spb/4 : self.spb * 3 / 4]
            average = sum(average_samples) / len(average_samples)
            if (average > thresh):
                bits.append(1)
            else:
                bits.append(0)

    # check the recieved preamble and compare to actual
    #COMMENTED OUT AS PER THE MILESTONE 3 INSTRUCTIONS!!!!
        #for i in range(0, preamble_len):
            #if preamble[i] != bits[i]:
                #print "\tPreamble was not detected"
                #print bits[0:preamble_len]
                #sys.exit(1)

        print "Received Preamble: " + str(bits[0:preamble_len])
        print ""
        return bits[preamble_len:] # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)

    def decode(self, rcd_bits):
        # decode the header
        header_len, header_index = common.get_coding_header_info()
        coded_header = rcd_bits[0:header_len * 3]
        header = self.hamming_decoding(coded_header, header_index, True)

        print "received coding header " + str(header)

        # Given the header bits, compute the length of coded bits
        # and encoding scheme

        index_bits = header[30:]
        length_bits = header[0:30]

        index_str = ""
        for bit in index_bits:
            index_str += str(bit)
        index = int(index_str, 2)

        length_str = ""
        for bit in length_bits:
            length_str += str(bit)
        length = int(length_str, 2)

        n = hamming.parameters[index][0]
        k = hamming.parameters[index][1]

        databits = self.hamming_decoding(rcd_bits[header_len * 3:], index, False)

        print "channel coding rate: " + str(k * 1.0 / n)

        return databits

    def hamming_decoding(self, coded_bits, index, is_header):

        n,k,H = hamming.parity_lookup(index)

        # split coded bits into chunks of size n (k message + (n-k) parity)
        len_coded_bits = len(coded_bits)
        coded_bits_split = [coded_bits[i:i+n] for i in range(0,len_coded_bits,n)]

        len_coded_bits_split = len(coded_bits_split)

        decoded_bits = list([])

        zero_syndrome = numpy.zeros(n-k, dtype=int)
        HT = numpy.transpose(H)

        num_errors = 0

        for i in range(0, len_coded_bits_split):
            syndrome = numpy.dot(H, numpy.transpose(coded_bits_split[i]))
            syndrome[:] = [x % 2 for x in syndrome]
            # syndrome is all zeros: no errors
            if numpy.array_equal(syndrome, zero_syndrome):
                decoded_bits.append(coded_bits_split[i][0:k])


            # if there's an error
            else:
                print "syndrome " + str(syndrome)

                error_loc = -1
                # figure out which column of H the syndrome corresponds with
                for j in range(0, k):
                    if numpy.array_equal(HT[j], syndrome):
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

        decoded_bits = numpy.array(decoded_bits)

        return decoded_bits.flatten()
