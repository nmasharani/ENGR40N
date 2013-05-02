import sys
import math
import numpy
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3

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
        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        ''' 
        return receiver_mil3.detect_threshold(demod_samples)

    def dotprod(self, arr1, arr2):
        if (len(arr1) != len(arr2)):
            return -1

        sum = 0.0;

        for i in range(0, len(arr1)):
            sum += arr1[i] * arr2[i]

        return sum

    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        
        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''

        energy_offset = -1

        for i in range(0, len(demod_samples) - self.spb):
            cur_samples = demod_samples[i:i+self.spb]
            average_samples = cur_samples[self.spb/4 : self.spb * 3 / 4]
            average = sum(average_samples) / len(average_samples)
            if (average >= (one + thresh)/2):
                energy_offset = i
                print energy_offset
                break

        if energy_offset < 0:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''
        # Fill in your implementation of the cross-correlation check procedure

        preamble = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]

        preamble_len = len(preamble)

        preamble_samples = list([])

        for bit in preamble:
            if (bit == 1):
                for i in range(0, self.spb):
                    preamble_samples.append(one)
            else:
                for i in range (0, self.spb):
                    preamble_samples.append(0.0)

        preamble_samples = numpy.array(preamble_samples)

        # Fill in your implementation of the high-energy check procedure

        correlation = list([])

        # range will go through the entire array of demodulated samples, stopping
        # when the remaining bits is too short to be the preamble
        for i in range (0, len(demod_samples) - len(preamble_samples) - energy_offset):
            current_range = demod_samples[i + energy_offset:i+len(preamble_samples) + energy_offset]
            correlation.append(self.dotprod(current_range, preamble_samples))

        maxindex = numpy.argmax(numpy.array(correlation))

        preamble_offset = maxindex
        print preamble_offset
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

        # Fill in your implementation

        return data_bits # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)
