import math
import common_txrx as common
import numpy as np

class Transmitter:
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
